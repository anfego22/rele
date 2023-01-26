import numpy as np
import torch
import torch.nn as nn
import pygame as pg
from math import prod
import ray
import parameters.enums as en


def actions_to_ohe(pressKey):
    return torch.Tensor(
        [int(pressKey[n]) for n in (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT)]
    )


def actions_to_plane(pressKey, dim: tuple = (60, 60)):
    """Convert a hot one encoded tensor into a plane of dims."""
    if len(pressKey) > prod(dim):
        raise Exception(f"Can't encode {len(pressKey)} vector into a {dim} matrix")
    res = [0] * prod(dim)
    for i, el in enumerate(pressKey):
        res[i] = 1 if el in (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT) else 0
    res = torch.Tensor(res)
    return res.reshape(dim)[None, :]


@ray.remote
class GameBuffer(object):
    """Class to store player history of moves."""

    def __init__(self, batchSize: int = 32, maxSize: int = None) -> None:
        self.history = []
        self.maxSize = maxSize if maxSize else float("inf")
        self.batchSize = batchSize
        self.importance = {}

    def add(self, data: dict) -> None:
        if len(self.history) > self.maxSize:
            self.history.pop(0)
        self.history.append(data)
        return None

    def get_sup_batch(self):
        if self.len() < self.batchSize:
            return None
        index = np.random.randint(0, len(self.history), self.batchSize)
        obs = torch.stack([self.history[i]["obs"] for i in index])
        act = torch.stack([self.history[i]["action"] for i in index])
        return (obs, act)

    def len(self) -> int:
        return len(self.history)

    def get_history(self, i: int):
        if abs(i) < self.len():
            return self.history[i]
        return None


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super().__init__()
        self.stride = stride
        self.in_planes = in_planes
        self.planes = planes
        self.block = nn.Sequential(
            nn.Conv2d(in_planes, planes, 3, stride, "same", bias=False),
            nn.BatchNorm2d(planes),
            nn.ReLU(),
            nn.Conv2d(planes, planes, 3, stride, "same", bias=False),
            nn.BatchNorm2d(planes),
            nn.ReLU(),
        )
        if stride != 1 or in_planes != self.expansion * planes:
            self.down = nn.Sequential(
                nn.Conv2d(
                    in_planes,
                    self.expansion * planes,
                    kernel_size=1,
                    padding="same",
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm2d(self.expansion * planes),
            )

    def forward(self, x):
        out = self.block(x)
        if self.stride != 1 or self.planes != self.in_planes:
            out = out + self.down(x)
        else:
            out = out + x
        out = nn.ReLU()(out)
        return out


class DownSample(nn.Module):
    def __init__(self, inpChannels: int, outChannels: int):
        super().__init__()
        self.down = nn.Sequential(
            nn.Conv2d(inpChannels, outChannels, 3, 1, "same"),
            BasicBlock(outChannels, outChannels),
            nn.AvgPool2d(3, 2, 1),
        )

    def forward(self, x: torch.Tensor):
        out = self.down(x)
        return out
