#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pkg_resources
data_path = pkg_resources.resource_filename('cnrgui', 'atten_data/')


class Material(object):
    '''
    Contains mass attenuation, thickness and density for a given material.
    '''

    def __init__(self, name, thickness=1, density=1):
        '''
        Parameters
        __________
        name : str
            Name of the material ('H2O', 'Os', 'U', 'P')
        thickness : float or int
            Thickness of material in CNR phantom, assumed to be in mm
        density : float or integer
            Density of material in CNR phantom, assumed to be in g/cm3

        Other Attributes
        ________________
        E_raw : ndarray
            Array of energy values in keV from NIST
        u_p_raw : ndarray
            Array of mass attenuation values in cm2/g from NIST
        E : ndarray
            Array of new energy values in keV, created after
            cnrgui.util.match_energies is called
        u_p : ndarray
            Array of interpolated mass attenuation values in cm2/g, 
            created after cnrgui.util.match_energies is called
        '''
        self.name = name
        self.fn = data_path + 'u_p_' + name + '.npy'
        self.E_raw, self.u_p_raw = self.__read_atten_data__(self.fn)
        self.thickness = thickness
        self.density = density
        self.E = None
        self.u_p = None

    def change_mat(self, name):
        '''
        Converts existing Material instance to a new material.
        '''
        self.name = name
        self.fn = data_path + 'u_p_' + name + '.npy'
        self.E_raw, self.u_p_raw = self.__read_atten_data__(self.fn)

    def __plot_u_p__(self):
        '''
        Displays mass attenuation plot
        '''
        plt.semilogy(self.E_raw, self.u_p_raw)
        plt.xlabel('E [keV]')
        plt.ylabel(r'$(\mu / \rho)$ [cm$^2$ / g]')
        plt.title('Mass Attenuation for {}'.format(self.name))
        plt.show()

    def __read_atten_data__(self, fn):
        '''
        Reads .npy filename, exports first (energy) and second (u/p, etc)
        columns as two numpy arrays
        '''

        data = np.load(fn)
        return data[:, 0], data[:, 1]
