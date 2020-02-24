from torch import nn

cfg = {
    'Small': [32, 'M', 64, 'M'],
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
}


class Classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.feature = self._make_layers(cfg['Small'])
        self.fc = nn.Linear(7 * 7 * 16, 512)
        self.classifier = nn.Linear(512, 9)

    def forward(self, x):

        out = self.feature(x)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        out = self.classifier(out)
        return out

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=5, padding=2),
                           nn.BatchNorm2d(x),
                           nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.Conv2d(in_channels, in_channels, kernel_size=3, padding=1), nn.BatchNorm2d(in_channels),
                   nn.ReLU(inplace=True)]
        layers += [nn.Conv2d(in_channels, 16, kernel_size=3, padding=1), nn.BatchNorm2d(16),
                   nn.ReLU(inplace=True)]
        return nn.Sequential(*layers)
