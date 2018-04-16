#!/usr/bin/env python

'''
This script provides a quick way to run a custom 1D CNR GUI. Customize the
allowable range of experimental parameters in the script below, then run
to launch.
'''

import numpy as np
from GUI_funcs import GUI

# Choose thickness units to be 'mm' or 'nm'
units = 'mm'

# Choose min and max sample thickness values (in units chosen above)
d_min = 0.0001
d_max = 2

# Choose min and max background material density range, in g/cc
bg_p_min = 0.5
bg_p_max = 1.5

# Choose min and max contrast material density range, in g/cc
c_p_min = 0.0001
c_p_max = 0.005

# Chose maximum intensity value, in number of photons
max_intensity_val = 1e5

# This creates and launches a GUI displaying CNR as a function of energy
# for parameter ranges chosen above
GUI(thickness_values=np.array([d_min, d_max]),
    bg_density_values=np.array([bg_p_min, bg_p_max]),
    contrast_density_values=np.array([c_p_min, c_p_max]),
    max_intensity_value=max_intensity_val,
    thickness_units=units)
