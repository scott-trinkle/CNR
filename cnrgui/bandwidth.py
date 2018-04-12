'''
WHAT TO DO AT BOUNDARIES
LOG INTERP OR LIN INTERP?
'''
from material import Material
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from time import time


def get_cnr(bg, contrast, I=1):

    conv = 0.1

    with np.errstate(over='ignore'):
        CNRtmp = np.sqrt(I) * contrast.u_p_int * \
            contrast.density / np.sqrt(np.exp(bg.u_p_int * bg.density * (bg.thickness * conv)) +
                                       np.exp(contrast.u_p_int * contrast.density * (contrast.thickness * conv) +
                                              bg.u_p_int * bg.density * (bg.thickness * conv)))
    CNR = np.where(CNRtmp > 1e-15, CNRtmp, 0)
    return CNR


# Initializing materials
h = Material('H2O',
             thickness=2,
             density=1)
os = Material('Os',
              thickness=0.1,
              density=0.005)
os.match_energies_with(h)

# Calculating monochromatic CNRs
mono_cnr = get_cnr(h, os)

# Initializing weights
# Based on sd = 1, truncating at truncate * sd, kernel size of n
tr = 4
n = 50
weights = np.exp(-0.5 * np.linspace(-tr, tr, n)**2)
weights /= weights.sum()

bw = 1e-2
bw_cnr = np.zeros_like(mono_cnr)
a = time()
for i, E in enumerate(h.E_int):
    sd = E * bw / (2*np.sqrt(2*np.log(2)))  # in keV
    w = tr * sd  # in keV
    Es = np.linspace(E-w, E+w, n)
    try:
        bw_cnr[i] = (weights * interp1d(h.E_int, mono_cnr)(Es)).sum()
    except ValueError:
        pass
b = time()
print('{} seconds'.format(b-a))
plt.plot(h.E_int, bw_cnr)
plt.show()

# def log_interp(x, y, x_new):
#     logx = np.log10(x)
#     logy = np.log10(y)
#     lin_interp = interp1d(logx, logy)

#     def log_interp(z):
#         return np.power(10.0, lin_interp(np.log10(z)))
#     return log_interp(x_new)
