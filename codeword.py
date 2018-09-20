class Codeword:
    """docstring for Codeword"""
    def __init__(self, V, A):
        self.V = V
        self.A = A

    def update(self, pixel, it):
        self.V[0] = (self.A[2] * self.V[0] + pixel.X[0]) / (self.A[2] + 1)
        self.V[1] = (self.A[2] * self.V[1] + pixel.X[1]) / (self.A[2] + 1)
        self.V[2] = (self.A[2] * self.V[2] + pixel.X[2]) / (self.A[2] + 1)

        self.A[0] = min(pixel.I, self.A[0])
        self.A[1] = max(pixel.I, self.A[1])
        self.A[2] += 1
        self.A[3] = max(self.A[3], it - self.A[5])
        self.A[5] = it
