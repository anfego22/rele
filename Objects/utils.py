import numpy as np
import pickle


class GameBuffer(object):
    """Class to store player history of moves."""

    def __init__(self, maxSize: int = 64) -> None:
        self.history = []
        self.maxSize = maxSize

    def add(self, X: np.array, action: int, score: int) -> None:
        if len(self.history) < self.maxSize:
            self.history.append((X, action))
            return None
        self.history.pop(0)
        self.history.append((X, action))

    def getLast(self):
        if len(self.history) > 0:
            return self.history[-1]
        return (None, None)
