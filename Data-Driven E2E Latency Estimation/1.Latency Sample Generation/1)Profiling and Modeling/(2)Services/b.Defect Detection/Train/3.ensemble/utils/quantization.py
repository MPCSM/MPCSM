import math
import torch

class Quantizer:
    def __init__(self, mask) -> None:
        super().__init__()
        self.max = 32  # use no more than 5 bit (2^5 -> 32) for storage
        self.mask = mask  # less than 5

    def quantify(self, activation_value):
        with torch.no_grad():
            rand = torch.rand(activation_value.shape).cuda() - 0.5
            activation = activation_value * self.max / 2
            compression_code = (activation / math.pow(2, self.mask) + rand).ceil()
            compression_code = torch.clamp(compression_code, 1 - math.pow(2, 4 - self.mask), math.pow(2, 4 - self.mask))
            eps = compression_code - activation_value
        compression = activation_value + eps
        return compression

    def restore(self, compression_code):
        with torch.no_grad():
            compression = compression_code * math.pow(2, self.mask)
            activation_value = compression / (self.max / 2)
            eps = activation_value - compression_code
        activation = compression_code + eps
        return activation