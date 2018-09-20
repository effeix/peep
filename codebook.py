class Codebook():
    """docstring for Codebook"""
    def __init__(self):
        self.codewords = []

    def empty(self):
        return len(self.codewords) == 0

    def __repr__(self):
        return f"Codebook({len(self.codewords)})"
