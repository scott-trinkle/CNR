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

# Thickness range, in mm
min_thickness = 0.1
max_thickness = 2

# Background material density range, in g / cc
min_bg_density = 0.5
max_bg_density = 1.5

# Contrast material density range, in g/cc
min_contrast_density = 0.0001
max_contrast_density = 0.005

# Maximum intensity value, in number of photons
max_intensity_val = 1e5

GUI(thickness_values=np.array([min_thickness, max_thickness]),
    bg_density_values=np.array([min_bg_density, max_bg_density]),
    contrast_density_values=np.array(
        [min_contrast_density, max_contrast_density]),
    max_intensity_value=max_intensity_val)
