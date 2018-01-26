import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


class Material(object):

    def __init__(self, name):
        self.name = name
        self.fn = 'atten_data/u_p_' + name + '.txt'
        self.E, self.u_p = read_atten_data(self.fn)

    def plot_u_p(self):
        plt.loglog(self.E, self.u_p)
        plt.xlabel('E [keV]')
        plt.ylabel(r'$(\mu / \rho)$ [cm$^2$ / g]')
        plt.title('Mass Attenuation for {}'.format(self.name))
        plt.show()

    def interp_u_p(self, new_E):
        return log_interp(self.E, self.u_p, new_E)


def read_atten_data(fn):
    '''
    Reads .txt filename, exports first (energy) and second (u/p, etc)
    columns as two numpy arrays
    '''

    data = np.loadtxt(fn, dtype=np.float64)
    data = data.reshape((data.size // 2, 2))
    return data[:, 0], data[:, 1]


def log_interp(xx, yy, xx_new):
    '''
    Import model input, model output, new input, returns log-interpolated
    output
    '''

    logx = np.log10(xx)
    logy = np.log10(yy)
    lin_interp = interpolate.interp1d(logx, logy)

    def log_interp(zz): return np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp(xx_new)


def match_arrays(bg, mat):
    '''
    Generates a common E vector for a given spectrum, metal and water.

    Finds the largest "minimum" energy and smallest "maximum" energy
    for all materials, since you cannot interpolate outside of the
    given data range.
    '''

    E_min = np.array([array.E.min() for array in [bg, mat]]).max()
    E_max = np.array([array.E.max() for array in [bg, mat]]).min()

    # Also finding the biggest "n" so that we don't lose any sharp detail
    n = np.array([array.E.size for array in [bg, mat]]).max()
    E = np.logspace(np.log10(E_min), np.log10(E_max), n)

    return E, bg.interp_u_p(E), mat.interp_u_p(E)


# bg = Material('H2O')
# mat = Material('Os')

# E, u_bg, u_mat = match_arrays(bg, mat)

# plt.close()


# D_mat = 0.01  # cm
# D_tot = 0.2  # cm
# D_bg = D_tot - D_mat  # cm
# p_bg = 1  # g/cc
# p_mat = np.array([0.0001, 0.0005, 0.001, 0.003, 0.005])  # g/cc

# # for p in p_mat:
# #     CNR = abs(u_bg * p_bg - u_mat * p) * \
# #         np.sqrt(np.exp(-u_bg * p_bg * D_bg - u_mat * p * D_mat))
# #     plt.plot(E, CNR, label='{}'.format(p))

# # plt.legend()
# # plt.xlim([0, 40])
# # plt.show()
