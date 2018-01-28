#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class Material(object):

    def __init__(self, name, thickness=None, density=None):
        self.name = name
        self.fn = '../atten_data/u_p_' + name + '.txt'
        self.E, self.u_p = read_atten_data(self.fn)
        self.thickness = thickness
        self.density = density

    def change_mat(self, name):
        self.name = name
        self.fn = '../atten_data/u_p_' + name + '.txt'
        self.E, self.u_p = read_atten_data(self.fn)

    def plot_u_p(self):
        plt.semilogy(self.E, self.u_p)
        plt.xlabel('E [keV]')
        plt.ylabel(r'$(\mu / \rho)$ [cm$^2$ / g]')
        plt.title('Mass Attenuation for {}'.format(self.name))
        plt.show()

    def match_energies_with(self, other_mat):
        '''
        Finds the largest "minimum" energy and smallest "maximum" energy
        for all materials, since you cannot interpolate outside of the
        given data range.
        '''

        E_min = np.array([mat.E.min() for mat in [self, other_mat]]).max()
        E_max = np.array([mat.E.max() for mat in [self, other_mat]]).min()

        # Also finding the biggest "n" so that we don't lose any sharp detail
        n = np.array([mat.E.size for mat in [self, other_mat]]).max()
        E = np.logspace(np.log10(E_min), np.log10(E_max), n)

        self.__interp_u_p__(E)
        other_mat.__interp_u_p__(E)

    def __interp_u_p__(self, new_E):
        self.E_int = new_E
        self.u_p_int = log_interp(self.E, self.u_p, new_E)


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
    lin_interp = interp1d(logx, logy)

    def log_interp(zz): return np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp(xx_new)


def match_energies(bg, contrast):
    '''
    Finds the largest "minimum" energy and smallest "maximum" energy
    for all materials, since you cannot interpolate outside of the
    given data range.
    '''

    E_min = np.array([mat.E.min() for mat in [bg, contrast]]).max()
    E_max = np.array([mat.E.max() for mat in [bg, contrast]]).min()

    # Also finding the biggest "n" so that we don't lose any sharp detail
    n = np.array([mat.E.size for mat in [bg, contrast]]).max()
    E = np.logspace(np.log10(E_min), np.log10(E_max), n)

    bg.interp_u_p(E)
    contrast.interp_u_p(E)

    return bg, contrast


def plot_1d(bg, contrast):
    plt.close()

    if hasattr(contrast.thickness, '__len__'):
        for d in contrast.thickness:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                               contrast.u_p_int * contrast.density * d))
            plt.plot(bg.E_int, CNR, label='{} mm {} length'.format(
                np.round(d, 3), contrast.name))

        plt.title('Contrast Thickness:\n{} g/cc {} density, {} g/cc {} density, {} mm {} length'.format(contrast.density,
                                                                                                        contrast.name,
                                                                                                        bg.density,
                                                                                                        bg.name,
                                                                                                        bg.thickness,
                                                                                                        bg.name))

    if hasattr(contrast.density, '__len__'):
        for p in contrast.density:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * p) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                               contrast.u_p_int * p * contrast.thickness))
            plt.plot(bg.E_int, CNR,
                     label='{} g/cc {} density'.format(np.round(p, 4), contrast.name))
        plt.title('Contrast density\n{} mm {} length, {} g/cc {} density, {} mm {} length'.format(contrast.thickness,
                                                                                                  contrast.name,
                                                                                                  bg.density,
                                                                                                  bg.name,
                                                                                                  bg.thickness,
                                                                                                  bg.name))

    if hasattr(bg.thickness, '__len__'):
        for d in bg.thickness:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * d -
                               contrast.u_p_int * contrast.density * contrast.thickness))
            plt.plot(bg.E_int, CNR, label='{} mm total'.format(
                np.round((d + 0.01) * 10, 3)))

        plt.title('Background thickness\n{} g/cc {} density, {} mm {} length, {} g/cc {} density'.format(contrast.density,
                                                                                                         contrast.name,
                                                                                                         contrast.thickness,
                                                                                                         contrast.name,
                                                                                                         bg.density,
                                                                                                         bg.name))

    if hasattr(bg.density, '__len__'):
        for p in bg.density:
            CNR = abs(bg.u_p_int * p - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * p * bg.thickness -
                               contrast.u_p_int * contrast.density * contrast.thickness))
            plt.plot(bg.E_int, CNR, label='{}'.format(np.round(p, 4)))

        plt.title('Background density\n{} g/cc {} density, {} mm {} length, {} mm {} length'.format(contrast.density,
                                                                                                    contrast.name,
                                                                                                    contrast.thickness,
                                                                                                    contrast.name,
                                                                                                    bg.thickness,
                                                                                                    bg.name))

    plt.xlabel('E [keV]')
    plt.ylabel('CNR')
    plt.legend()
    plt.xlim([0, 40])


def parameter_string(index):
    if index == 1:
        return 'Energy'
    if index == 2:
        return 'Contrast material'
    if index == 3:
        return 'Contrast thickness'
    if index == 4:
        return 'Contrast density'
    if index == 5:
        return 'Background material'
    if index == 6:
        return 'Background thickness'
    if index == 7:
        return 'Background density'


def get_param_range(index):

    # TAKE OUT CHOICE FOR N, THAT'S DECIDED BY DATA

    if index == 1:  # Energy
        E_kill = False
        while E_kill == False:
            E_range_str = input(
                '\nEnter the low and high energy values in keV, and the number of energy steps (E_low,E_high,n): ')
            try:
                E_low, E_high, n = [float(i) for i in E_range_str.split(',')]
            except ValueError:
                print(
                    '\nError - Please enter three comma-separated values (E_low,E_high,n)')
            else:
                if E_low >= E_high:
                    print('\nError - E_low cannot be larger than E_high')
                if n <= 1:
                    print('\nError - n must be > 1')
                else:
                    return np.linspace(E_low, E_high, n)
