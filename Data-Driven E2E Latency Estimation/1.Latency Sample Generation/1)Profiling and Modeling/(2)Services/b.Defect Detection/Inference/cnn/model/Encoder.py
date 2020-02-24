import math
from time import sleep

import torch

from torch import nn
import torch.nn.functional as F

from utils.quantization import Quantizer

# cfg = {
#     '3-12': [16, 108, 106]
# }

mask = 4


class Encoder(nn.Module):
    def __init__(self, mask):
        super().__init__()
        self.encoded = None
        self.features = self._convolutional_layer()
        self.mask = mask
        self.quantizer = Quantizer(self.mask)

    def forward(self, x):
        # if self.training:
        #     noise = torch.randn(x.size())/32
        #     x += noise.cuda()
        out = self.features(x)
        # if self.training:
        #     with torch.no_grad():
        #         
        #         rand = torch.rand(out.shape).cuda()
        #         prob = 0.5 + out
        #         eps = torch.zeros(out.shape).cuda()
        #         eps[rand <= prob] = (1 - out)[rand <= prob]
        #         eps[rand > prob] = (-out - 1)[rand > prob]
        #     self.encoded = 0.5 * (out + eps + 1)
        # else:
        #     self.encoded = out.ceil()
        if self.training:
            self.encoded = self.quantizer.quantify(out)
        else:
            self.encoded = (out * math.pow(2, 4 - self.mask)).ceil()

        return self.encoded

    def _convolutional_layer(self):
        layers = []
        layers += [nn.Conv2d(3, 16, kernel_size=5, stride=1, padding=2), nn.BatchNorm2d(16), nn.LeakyReLU(inplace=True)]
        layers += [nn.Conv2d(16, 32, kernel_size=5, stride=2, padding=2), nn.BatchNorm2d(32), nn.LeakyReLU(inplace=True)]
        layers += [nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1), nn.BatchNorm2d(32), nn.LeakyReLU(inplace=True)]
        layers += [nn.Conv2d(32, 6, kernel_size=3, padding=1), nn.BatchNorm2d(6), nn.Tanh()]
        return nn.Sequential(*layers)
