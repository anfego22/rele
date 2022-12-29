import numpy as np
import torch
import torch.nn as nn


class GameBuffer(object):
    """Class to store player history of moves."""

    def __init__(self, maxSize: int = 64) -> None:
        self.history = []
        self.maxSize = maxSize

    def add(self, data: dict) -> None:
        if len(self.history) < self.maxSize:
            self.history.append(data)
            return None
        self.history.pop(0)
        self.history.append(data)

    def getLast(self):
        if len(self.history) > 0:
            return self.history[-1]
        return {}


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super().__init__()
        self.stride = stride
        self.block = nn.Sequential(
            nn.Conv2d(
                in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
            ),
            nn.BatchNorm2d(planes),
            nn.ReLU(),
            nn.Conv2d(planes, planes, kernel_size=3, padding=1, stride=1, bias=False),
            nn.BatchNorm2d(planes),
            nn.ReLU(),
        )
        if stride != 1 or in_planes != self.expansion * planes:
            self.down = nn.Sequential(
                nn.Conv2d(
                    in_planes,
                    self.expansion * planes,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm2d(self.expansion * planes),
            )

    def forward(self, x):
        out = self.block(x)
        if self.stride != 1:
            out = out + self.down(x)
        else:
            out = out + x
        out = nn.ReLU()(out)
        return out


class DownSample(nn.Module):
    def __init__(self, inpChannels: int, outChannels: int):
        super().__init__()
        self.down = nn.Sequential(
            nn.Conv2d(inpChannels, outChannels, 3, 1),
            BasicBlock(outChannels, outChannels),
            nn.AvgPool2d(3, 2, 1),
        )

    def forward(self, x: torch.Tensor):
        out = self.down(x)
        return out
