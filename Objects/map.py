import pygame as pg
import parameters.enums as en


class Map:
    def __init__(self, filename: str) -> None:
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line)

        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * en.TILE_SIZE
        self.height = self.tileHeight * en.TILE_SIZE
