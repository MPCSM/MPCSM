import math

from torch import nn

from utils.quantization import Quantizer

# cfg = {
#     '3-12': [1, 116, 108],
# }

class Decoder(nn.Module):
    def __init__(self, mask):
        super().__init__()
        self.decode = self._comp_layer()
        self.mask = mask
        self.quantizer = Quantizer(self.mask)

    def forward(self, x):
        x = self.quantizer.restore(x)
        picture = self.decode(x)
        return picture

    def _comp_layer(self):
        layers = []
        layers += [nn.Conv2d(6, 16, kernel_size=3, padding=1), nn.BatchNorm2d(16), nn.LeakyReLU(inplace=True)]
        layers += [nn.ConvTranspose2d(16, 32, kernel_size=2, stride=2, padding=0), nn.BatchNorm2d(32), nn.LeakyReLU(inplace=True)]
        layers += [nn.ConvTranspose2d(32, 32, kernel_size=2, stride=2, padding=0), nn.BatchNorm2d(32), nn.LeakyReLU(inplace=True)]
        layers += [nn.Conv2d(32, 3, kernel_size=3, padding=1), nn.LeakyReLU(inplace=True)]

        return nn.Sequential(*layers)
