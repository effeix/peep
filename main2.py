import argparse
import os
import random
from math import sqrt

import cv2
import matplotlib.pyplot as plt
import numpy as np

from codebook import Codebook
from codeword import Codeword
from pixel import Pixel


BASE_PATH = os.path.dirname(__file__)
TRAINING_PATH = os.path.abspath(os.path.join(BASE_PATH, "../images/Crowd_PETS09/S0/Background/View_001/Time_13-06/"))
EPSILON_1 = 1
TRAIN_N_IMG = 10


if __name__ == '__main__':

    img_list = os.listdir(TRAINING_PATH)[:TRAIN_N_IMG]
    
    for it, file in enumerate(img_list):

        img = cv2.cvtColor(
            cv2.imread(
                os.path.join(
                    TRAINING_PATH,
                    file
                )
            ),
            cv2.COLOR_BGR2RGB
        ).astype(float)

        if it == 0:
            codebooks = np.array(
                [Codebook() for pixel in range(img.shape[0] * img.shape[1])]
            )

        for px_row in img:
            for px_idx, px in enumerate(px_row):

                R = px[0]
                G = px[1]
                B = px[2]
                X = np.array([R, G, B])
                I = sqrt(R**2 + G**2 + B**2)
                pixel = Pixel(X, I)

                codebook_empty = True
                no_match = True
                
                for codeword in codebooks[px_idx].codewords:
                    codebook_empty = False

                    if pixel.match(codeword, alpha, beta, epsilon):
                        codeword.update(pixel, it)
                        no_match = False
                        
                        break

                if codebook_empty or no_match:
                    A = np.array([pixel.I, pixel.I, 1, it, it+1, it+1])
                    new_codeword = Codeword(pixel.X, A)
                    codebooks[px_idx].codewords.append(new_codeword)
