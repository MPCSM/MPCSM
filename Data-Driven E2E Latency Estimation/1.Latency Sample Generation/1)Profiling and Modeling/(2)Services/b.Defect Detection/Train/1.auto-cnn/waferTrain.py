import argparse
import math
import os
from random import random
from time import sleep
import pandas as pd

import torch
import torchvision
from torch import nn, optim
from torch.backends import cudnn
from torchvision import transforms

from model.Classifier import Classifier
from model.Decoder import Decoder
from model.Encoder import Encoder
from utils.progress_bar import progress_bar
os.environ["CUDA_VISIBLE_DEVICES"] = '1'

def normalize(tensor, mean, std):
    for t, m, s in zip(tensor, mean, std):
        t.sub_(m).div_(s)
    return tensor


attenuation = 48
learning_rate = 0.1
mask = 0
codir = str(attenuation) + '_' + str(mask)

parser = argparse.ArgumentParser(description='PyTorch Emnist Training')
parser.add_argument('--lr', default=learning_rate, type=float, help='learning rate')
parser.add_argument('--resume', '-r', action='store_true', help='resume from checkpoint')
args = parser.parse_args()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
best_loss = 99999  # best test accuracy
start_epoch = 0  # start from epoch 0 or last checkpoint epoch
if not os.path.isfile('./dataframe/result_'+codir+'.csv'):
    save_df = pd.DataFrame(columns=('epoch', 'MSE_loss', 'classifier_loss', 'accuracy'))
else:
    save_df = pd.read_csv('./dataframe/result_'+codir+'.csv')

# Data
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])

transform_train2 = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),

])

transform_test = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])

transform_test2 = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.ImageFolder(root='./data/Training', transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=256, shuffle=True, num_workers=2)

testset = torchvision.datasets.ImageFolder(root='./data/Test', transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=200, shuffle=False, num_workers=2)

# Mode
print('==> Building model..')
encoder = Encoder(mask=mask)
decoder = Decoder(mask=mask)
classifier = Classifier()
encoder = encoder.to(device)
decoder = decoder.to(device)
classifier = classifier.to(device)
if device == 'cuda':
    cudnn.benchmark = True
if args.resume:
    # Load checkpoint.
    print('==> Resuming from checkpoint..')
    assert os.path.isdir('checkpoint'), 'Error: no checkpoint directory found!'
    checkpoint = torch.load('./checkpoint/ckpt_'+codir+'.t7')
    encoder.load_state_dict(checkpoint['encoder'])
    decoder.load_state_dict(checkpoint['decoder'])
    classifier.load_state_dict(checkpoint['classifier'])
    best_loss = checkpoint['loss']
    start_epoch = checkpoint['epoch']

# # in the cloud
# for param in encoder.parameters():
#     param.requires_grad = False

criterion1 = nn.MSELoss()
criterion2 = nn.CrossEntropyLoss()
optimizer1 = optim.SGD(encoder.parameters(), lr=args.lr, momentum=0.9, weight_decay=9e-4)
optimizer2 = optim.SGD(decoder.parameters(), lr=args.lr, momentum=0.9, weight_decay=9e-4)
optimizer3 = optim.SGD(classifier.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4)

# Training
def train(epoch):
    print('\nEpoch: %d' % epoch)
    encoder.train()
    decoder.train()
    classifier.train()
    train_loss1 = 0
    train_loss2 = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer1.zero_grad()
        optimizer2.zero_grad()
        optimizer3.zero_grad()
        feature = encoder(inputs)
        picture = decoder(feature)
        picture_ = picture.data.detach().cpu()
        input_pic = torch.Tensor(normalize(picture_, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))).to(device)
        input_pic.requires_grad = True
        y = classifier(input_pic)
        loss1 = criterion1(picture, inputs)
        loss2 = criterion2(y, targets)
        loss1.backward(retain_graph=True)
        if attenuation != "nc":
            loss2.backward()
            picture.backward(input_pic.grad / attenuation)
        optimizer1.step()
        optimizer2.step()
        optimizer3.step()

        train_loss1 += loss1.item()
        train_loss2 += loss2.item()
        _, predicted = y.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        progress_bar(batch_idx, len(trainloader), 'Loss1: %.3f | Loss2: %.3f | Acc: %.3f%% (%d/%d)' %
                     (train_loss1 / (batch_idx + 1), train_loss2 / (batch_idx + 1), 100. * correct / total, correct, total))


# Training
def test(epoch):
    global best_loss
    global save_df
    encoder.eval()
    decoder.eval()
    classifier.eval()
    train_loss1 = 0
    train_loss2 = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(testloader):
        # print_real_pic(inputs)
        inputs, targets = inputs.to(device), targets.to(device)
        feature = encoder(inputs)
        picture = decoder(feature)
        # print_comp_pic(picture.cpu())
        # print('Done.')
        # sleep(1000)
        picture_ = picture.data.detach().cpu()
        input_pic = torch.Tensor(normalize(picture_, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))).to(device)
        y = classifier(input_pic)
        loss1 = criterion1(picture, inputs)
        loss2 = criterion2(y, targets)


        train_loss1 += loss1.item()
        train_loss2 += loss2.item()
        _, predicted = y.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        progress_bar(batch_idx, len(testloader), 'Loss1: %.6f | Loss2: %.4f | Acc: %.3f%% (%d/%d)'
                     % (train_loss1 / (batch_idx + 1), train_loss2 / (batch_idx + 1), 100. * correct / total,
                        correct, total))

        if batch_idx == 585:
            save_df = save_df.append(pd.DataFrame({'epoch': epoch, 'MSE_loss': train_loss1 / (batch_idx + 1),
                                                   'classifier_loss': train_loss2 / (batch_idx + 1),
                                                   'accuracy': correct / total}, index=[0]))
            if not os.path.isdir('dataframe'):
                os.mkdir('dataframe')
            save_df.to_csv('./dataframe/result_' + codir + '.csv', index=False)

    # Save checkpoint.
    acc = 100. * correct / total
    if train_loss1 < best_loss:
        print('Saving..')
        state = {
            'encoder': encoder.state_dict(),
            'decoder': decoder.state_dict(),
            'classifier': classifier.state_dict(),
            'loss': train_loss1,
            'epoch': epoch,
        }
        if not os.path.isdir('checkpoint'):
            os.mkdir('checkpoint')
        torch.save(state, './checkpoint/ckpt_'+codir+'.t7')
        best_loss = train_loss1

def print_real_pic(pic):
    for index, single_pic in enumerate(pic):
        single_pic = torch.clamp(single_pic, min=0, max=1)
        single_pic = transforms.ToPILImage()(single_pic).convert('RGB')
        if not os.path.isdir('pic'):
            os.mkdir('pic')
        single_pic.save('./pic/' + str(index) + 'real_img.png')

def print_comp_pic(pic):
    for index, single_pic in enumerate(pic):
        single_pic = torch.clamp(single_pic, min=0, max=1)
        single_pic = transforms.ToPILImage()(single_pic).convert('RGB')
        if not os.path.isdir('pic'):
            os.mkdir('pic')
        single_pic.save('./pic/' + str(index) + 'comp_img.png')

if __name__ == '__main__':
    for epoch in range(start_epoch, start_epoch+100):
        train(epoch)
        test(epoch)

