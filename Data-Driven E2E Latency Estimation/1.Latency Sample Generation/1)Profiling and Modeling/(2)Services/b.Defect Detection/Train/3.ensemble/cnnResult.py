from scipy import interpolate
from skimage import measure
from scipy import stats
from skimage.transform import radon
import torch
from bitarray import bitarray
from torchvision.transforms.functional import to_tensor

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'
mask = 4
codir = str(mask)
mapping_type = {0: 'Center', 1: 'Donut', 2: 'Edge-Loc', 3: 'Edge-Ring', 4: 'Loc', 5: 'Near-full', 6: 'Random',
                7: 'Scratch', 8: 'none'}

coder = torch.load('encoder_' + codir + '.pth').to(device)
classifier = torch.load('classifier_' + codir + '.pth').to(device)

# Image features are extracted from the encoder and converted into compressed bitmaps for transmission
def feature_extract(img):
    # Get single image input

    input = to_tensor(img).unsqueeze(0)

    # Get a single image feature extraction

    feature = coder(input)
    wafermap = np.array(feature.cpu().detach(), dtype='int8')
    bitmaps = []
    for _ in range(5 - mask):
        bitmap = wafermap % 2
        wafermap = wafermap // 2
        bitmaps.append(bitmap)
    bitmaps = np.array(bitmaps[::-1])
    bitarrs = bitarray(bitmaps.flatten().tolist())
    return bitarrs




# Decode bitmaps and classify them
def classify(feature_bitarrs):
    wafer = np.array(feature_bitarrs.tolist())
    wafer.resize((5 - mask, 6, 7, 7))
    feature = np.zeros((6, 7, 7))
    for index in wafer:
        feature = feature * 2 + index
    feature = torch.Tensor(feature).unsqueeze(0)

    y = classifier(feature).detach()
    label = int(np.argmax(y.data.numpy()[0]))
    #label = mapping_type[int(np.argmax(label))]
    return label


if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    from PIL import Image
    import pickle

    attributes = ["cnnResult"]
    labels = ["result"]
    attriContent = []
    resultConet = []

    # Convert data into pictures
    df = pd.read_pickle("./wafermap_withlabel.pkl")
    df_withlabel = df.reset_index()
    for index, row in df_withlabel.iterrows():
        usage = str(row['trianTestLabel'][0][0])
        category = str(row['failureType'][0][0])
        resultConet.append(category)
        # auto cnn
        color = np.array([(row['waferMap'] == 2) * 240 + (row['waferMap'] == 1) * 94 + (row['waferMap'] == 0) * 255,
                          (row['waferMap'] == 2) * 168 + (row['waferMap'] == 1) * 204 + (
                                  row['waferMap'] == 0) * 255,
                          (row['waferMap'] == 2) * 60 + (row['waferMap'] == 1) * 204 + (
                                  row['waferMap'] == 0) * 255])
        color = np.swapaxes(color, 2, 0)
        img = Image.fromarray(color.astype(np.uint8), 'RGB').resize((28, 28))
        feature_bitarr = feature_extract(img)
        cnnResult = classify(feature_bitarr)

        # 合并
        attriContent.append(cnnResult)

waferattributes = pd.DataFrame(columns=attributes, data=attriContent)
waferlabels = pd.DataFrame(columns=labels, data=resultConet)
waferattributes.to_csv("wafercnnAttribute.csv")
waferlabels.to_csv("waferResult.csv")
