import torch
import torch.nn as nn
import Objects.utils as ut
import parameters.enums as en
from math import prod
import torch.optim as optim


class Supervised(nn.Module):
    def __init__(self, inputDim: list, actionSpace: int):
        super().__init__()
        inpChannel = inputDim[0]
        self.outDim = actionSpace
        self.down = nn.Sequential(
            ut.BasicBlock(inpChannel, inpChannel * 2),
            ut.DownSample(inpChannel * 2, inpChannel * 2),
            ut.BasicBlock(inpChannel * 2, inpChannel),
            ut.DownSample(inpChannel, inpChannel // 2),
        )
        linInp = [inpChannel // 2, inputDim[1] // (2**2), inputDim[2] // (2**2)]
        linInp = prod(linInp)
        self.linear = nn.Sequential(
            nn.Linear(linInp, linInp // 2),
            nn.ReLU(),
            nn.Linear(linInp // 2, self.outDim),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor):
        out = self.down(x)
        out = nn.Flatten(1)(out)
        out = self.linear(out)
        return out


class Brain(object):
    def __init__(self, inputDim: list, actionSpace: int):
        self.channels = inputDim[0]
        self.prevObs = en.PREV_OBS
        self.dim0 = (inputDim[0] + 1) * en.PREV_OBS
        self.inputDim = [self.dim0] + inputDim[1:]
        self.actionSpace = actionSpace
        self.supe = Supervised(self.inputDim, self.actionSpace)
        self.optim = optim.Adam(self.supe.parameters(), lr=1e-4, weight_decay=1e-5)

    def train(self, batch: dict):
        aHat = self.supe(batch["obs"])
        loss = nn.CrossEntropyLoss()(aHat, batch["action"])

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
        self.supe.eval()
        return loss

    def act(self, obs: torch.Tensor):
        with torch.no_grad():
            logits = self.supe(obs)
            return nn.Softmax(1)(logits).numpy()
