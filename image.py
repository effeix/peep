from codebook import Codebook
from copy import deepcopy

class Image:
    def __init__(self, shape):
        self.codebooks = []
        self.height = shape[1]
        self.width = shape[0]

        for i in range(self.width):
            for j in range(self.height):
                self.codebooks.append(Codebook())

    def get_codebooks():
        return self.codebooks
