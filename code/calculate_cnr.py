import numpy as np
import matplotlib.pyplot as plt
from misc_funcs import Material, generate_materials, plot_1d

bg_mat = 'H2O'
bg_thickness = 0.2  # cm
# bg_thickness = np.array([1, 2, 3, 4, 5]) * 0.1 - 0.01
bg_density = 1.0  # g/cc
# bg_density = [0.1, 0.5, 1.0, 2.0]
bg_specs = [bg_mat, bg_thickness, bg_density]

contrast_mat = 'Os'
contrast_thickness = 0.01
# contrast_thickness = [0.01, 0.02, 0.05]  # cm
# contrast_density = 0.0001
contrast_density = [0.0001, 0.0005, 0.001, 0.003, 0.005]
contrast_specs = [contrast_mat, contrast_thickness, contrast_density]

bg, contrast = generate_materials(bg_specs, contrast_specs)

'''
 'Energy'
 0'Contrast material'
 'Contrast thickness'
 'Contrast density'
 'Background material'
 'Background thickness'
 'Background density'
'''

plot_1d(bg, contrast)
