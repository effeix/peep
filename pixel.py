class Pixel:
    def __init__(self, X, I):
        self.X = X
        self.I = I

    def match(self, codeword, alpha=0.55, beta=1.3, epsilon=1):
        if self._color_distortion(codeword) < epsilon \
            and self._brightness(codeword, alpha, beta):
            print("Match")

    def _color_distortion(self, other_codeword):
        mod_Xt_squared = sum([i**2 for i in self.X])
        mod_Vm_squared = sum([i**2 for i in codeword.v])
        inner_prod_squared = sum([Xt[i]*Vm[i] for i in range(len(Vm))])**2
    
        if mod_Vm_squared == 0.0:
            p_squared = 0.0
        else:
            p_squared = inner_prod_squared / mod_Vm_squared
        
        return sqrt(mod_Xt_squared - p_squared)

    def _brightness(self, codeword, alpha, beta):
        Imin = codeword.aux[0]
        Imax = codeword.aux[1]

        return Imax*alpha <= self.I <= min(beta*Imax, Imin/alpha)

