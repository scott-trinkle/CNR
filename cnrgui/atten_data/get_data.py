import numpy as np
import pandas as pd
from urllib.parse import urlencode


def get_NIST_data(mat, lower=0, upper=100):
    '''
    Scrapes mass attenuation data for an element or material
    from the NIST X-ray Form Factor, Attenuation and Scattering
    Tables (FFAST)

    https://physics.nist.gov/PhysRefData/FFast/html/form.html

    Parameters
    __________
    mat : str or int
        Atomic number (Z) if int, material name if str
    lower : float or int
        Lower bound on energy range
    upper : float or int
        Upper bound on energy range (Note, FFAST only goes to 433 keV)

    Returns
    _______
    data : (N, 2) ndarray
        Mass attenuation data for 'mat'. data[:,0] is the energy in keV,
        data[:,1] is the mass attenuation in cm2/g
    '''

    baseurl = 'https://physics.nist.gov/cgi-bin/ffast/ffast.pl?'

    # Parses 'mat' input and sets Z and Formula paramters accordingly
    Z, Formula = (str(mat), '') if type(mat) == int else ('', str(mat))

    params = {'Z': Z,
              'Formula': Formula,
              'gtype': '3',  # Indicates mass attenuation tables
              'range': 'S',
              'lower': str(lower),
              'upper': str(upper),
              'density': '',
              'frames': 'no',
              'htmltable': '1'}

    # Returns a list of html tables as a pandas dataframe.
    # For these pages, there is only one html table, so we return the
    # first one and save as ndarray with ".values"
    data = pd.read_html(baseurl + urlencode(params), header=0)[0].values
    return data


# Getting data for Osmium, Lead, Uranium and Water
materials = [76, 82, 92, 'H2O']
names = ['Os', 'Pb', 'U', 'H2O']

for mat, name in zip(materials, names):
    np.save('u_p_' + name, get_NIST_data(mat))
