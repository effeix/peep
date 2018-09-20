import argparse
import os
import random
from math import sqrt

import cv2
import matplotlib.pyplot as plt
import numpy as np

from codebook import Codebook
from codeword import Codeword
from image import Image


BASE_PATH = os.path.dirname(__file__)
TRAINING_PATH = os.path.abspath(os.path.join(BASE_PATH, "../images/Crowd_PETS09/S0/Background/View_001/Time_13-06/"))
EPSILON_1 = 1

VM = 0
AUX = 1
R_CH = 0
G_CH = 1
B_CH = 2
I_MIN = 0
I_MAX = 1
FM = 2
LAMBDA = 3
P = 4
Q = 5

np.seterr("raise")

class Codeword:
    def __init__(self):
        self.rgb = []
        self.aux = []

def colordist(Xt, Vm):
    """
    mod_Xt = ||Xt||^2 = R^2 + G^2 + B^2
    
    mod_Vm = ||Vm||^2 = Rm^2 + Gm^2 + Bm^2
    
    inner_prod_squared = (R*Rm + G*Gm + B*Bm)^2
    
    p_squared = (R*Rm + G*Gm + B*Bm)^2
                ----------------------
                  Rm^2 + Gm^2 + Bm^2
                 ____________________
    colordist = /||Xt||^2 - p_squared
    """
    mod_Xt = sum([i**2 for i in Xt])
    mod_Vm = sum([i**2 for i in Vm])
    inner_prod_squared = sum([Xt[i]*Vm[i] for i in range(len(Vm))])**2
    
    if mod_Vm == 0.0:
        p_squared = 0.0
    else:
        p_squared = inner_prod_squared / mod_Vm
    
    return sqrt(mod_Xt - p_squared)

def brightness(I, Imin, Imax, alpha, beta):
    return alpha*Imax <= I <= min(beta*Imax, Imin / alpha)

def match(x, v, I, Imin, Imax):
    return colordist(x, v) < EPSILON_1 and brightness(I, Imin, Imax) 


if __name__ == '__main__':

    it = -1
    px_idx = -1

    for file in os.listdir(TRAINING_PATH)[:10]:
        it += 1

        img_path = os.path.join(TRAINING_PATH, file)
    
        img = cv2.cvtColor(
            cv2.imread(img_path),
            cv2.COLOR_BGR2RGB
        ).astype(float)

        if it == 0:
            codebooks = []

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    codebooks.append([])

        for row in img:
            for px in row:
                px_idx += 1

                R = px[0]
                G = px[1]
                B = px[2]

                Xt = [R, G, B]
                I = sqrt(R**2 + G**2 + B**2)

                if not codebooks[px]:
                    new_codeword = []
                    new_codeword.append(Xt)
                    new_codeword.append([I, I, 1, it, it+1, it+1])
                    codebooks[px].append(new_codeword)

                else:
                    for cw in codebooks[px]:
                        if match(Xt, cw[VM], I, cw[AUX][I_MIN], cw[AUX][I_MAX]):
                            cw[VM][R_CH] = (cw[AUX][FM] * cw[VM][R_CH] + R) / (cw[AUX][FM] + 1)
                            cw[VM][G_CH] = (cw[AUX][FM] * cw[VM][G_CH] + G) / (cw[AUX][FM] + 1)
                            cw[VM][B_CH] = (cw[AUX][FM] * cw[VM][B_CH] + B) / (cw[AUX][FM] + 1)

                            cw[AUX][I_MIN] = min(I, cw[AUX][I_MIN])
                            cw[AUX][I_MAX] = max(I, cw[AUX][I_MAX])
                            cw[AUX][FM] += 1
                            cw[AUX][LAMBDA] = max(cw[AUX][LAMBDA], it - cw[AUX][Q])
                            cw[AUX][Q] = it

                            break

                        else:
                            new_codeword = []
                            new_codeword.append(Xt)
                            new_codeword.append([I, I, 1, it - 1, it, it])
                            codebooks[px].append(new_codeword)
