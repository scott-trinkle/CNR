#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class Material(object):

    def __init__(self, name, thickness=None, density=None):
        self.name = name
        self.fn = 'atten_data/u_p_' + name + '.npy'
        self.E, self.u_p = self.__read_atten_data__(self.fn)
        self.thickness = thickness
        self.density = density

    def change_mat(self, name):
        self.name = name
        self.fn = 'atten_data/u_p_' + name + '.npy'
        self.E, self.u_p = self.__read_atten_data__(self.fn)

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
        self.u_p_int = self.__log_interp__(self.E, self.u_p, new_E)

    def __read_atten_data__(self, fn):
        '''
        Reads .npy filename, exports first (energy) and second (u/p, etc)
        columns as two numpy arrays
        '''

        data = np.load(fn)
        return data[:, 0], data[:, 1]

    def __log_interp__(self, xx, yy, xx_new):
        '''
        Import model input, model output, new input, returns log-interpolated
        output
        '''

        logx = np.log10(xx)
        logy = np.log10(yy)
        lin_interp = interp1d(logx, logy)

        def log_interp(zz): return np.power(10.0, lin_interp(np.log10(zz)))
        return log_interp(xx_new)
