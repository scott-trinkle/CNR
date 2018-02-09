'''
This script provides a quick way to run a custom 1D CNR GUI. Customize the
allowable range of experimental parameters in the script below, then run
to launch. 
'''

import numpy as np
from GUI_funcs import GUI
import os

try:
    # Sets correct path when running from command line so that attenuation data
    # is loaded properly
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
except NameError:
    # Retains functionality when sending code directly to interpreter (i.e. when
    # testing using emacs python shell)
    pass


# Choose thickness units to be 'mm' or 'nm'
units = 'mm'

# Choose min and max sample thickness values (in units chosen above)
min_thickness = 0.1
max_thickness = 2

# Choose min and max background material density range, in g / cc
min_bg_density = 0.5
max_bg_density = 1.5

# Choose min and max contrast material density range, in g/cc
min_contrast_density = 0.0001
max_contrast_density = 0.005

# Chose maximum intensity value, in number of photons
max_intensity_val = 1e5

# This creates and launches a GUI displaying CNR as a function of energy
# for parameter ranges chosen above
GUI(thickness_values=np.array([min_thickness, max_thickness]),
    bg_density_values=np.array([min_bg_density, max_bg_density]),
    contrast_density_values=np.array(
        [min_contrast_density, max_contrast_density]),
    max_intensity_value=max_intensity_val,
    thickness_units=units)
