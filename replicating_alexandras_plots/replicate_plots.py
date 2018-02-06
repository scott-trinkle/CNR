import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../code/')
from misc_funcs import Material


def plot_1d(bg, contrast):
    plt.close()

    if hasattr(contrast.thickness, '__len__'):
        for d in contrast.thickness:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                               contrast.u_p_int * contrast.density * d))
            plt.plot(bg.E_int, CNR, label='{} mm {} length'.format(
                np.round(d, 3) * 10, contrast.name))

        plt.title('Contrast Thickness:\n{} g/cc {} density, {} g/cc {} density, {} mm {} length'.format(contrast.density,
                                                                                                        contrast.name,
                                                                                                        bg.density,
                                                                                                        bg.name,
                                                                                                        bg.thickness * 10,
                                                                                                        bg.name))

    if hasattr(contrast.density, '__len__'):
        for p in contrast.density:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * p) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                               contrast.u_p_int * p * contrast.thickness))
            plt.plot(bg.E_int, CNR,
                     label='{} g/cc {} density'.format(np.round(p, 4), contrast.name))
        plt.title('Contrast density\n{} mm {} length, {} g/cc {} density, {} mm {} length'.format(contrast.thickness * 10,
                                                                                                  contrast.name,
                                                                                                  bg.density,
                                                                                                  bg.name,
                                                                                                  bg.thickness * 10,
                                                                                                  bg.name))

    if hasattr(bg.thickness, '__len__'):
        for d in bg.thickness:
            CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * bg.density * d -
                               contrast.u_p_int * contrast.density * contrast.thickness))
            plt.plot(bg.E_int, CNR, label='{} mm total'.format(
                np.round((d + contrast.thickness) * 10, 3)))

        plt.title('Total thickness\n{} g/cc {} density, {} mm {} length, {} g/cc {} density'.format(contrast.density,
                                                                                                    contrast.name,
                                                                                                    contrast.thickness * 10,
                                                                                                    contrast.name,
                                                                                                    bg.density,
                                                                                                    bg.name))

    if hasattr(bg.density, '__len__'):
        for p in bg.density:
            CNR = abs(bg.u_p_int * p - contrast.u_p_int * contrast.density) * \
                np.sqrt(np.exp(-bg.u_p_int * p * bg.thickness -
                               contrast.u_p_int * contrast.density * contrast.thickness))
            plt.plot(
                bg.E_int, CNR, label='{} g/cc {} density'.format(np.round(p, 4), bg.name))

        plt.title('Background density\n{} g/cc {} density, {} mm {} length, {} mm {} length'.format(contrast.density,
                                                                                                    contrast.name,
                                                                                                    contrast.thickness * 10,
                                                                                                    contrast.name,
                                                                                                    bg.thickness * 10,
                                                                                                    bg.name))

    plt.xlabel('E [keV]')
    plt.ylabel('CNR')
    plt.legend()
    plt.xlim([0, 40])


'''
For all:
Contrast thickness: 0.1 mm

Graph 1: 
Os
Total length: 2 mm
p = [0.0001, 0.0005, 0.001, 0.003, 0.005]

Graph 2: 
Same but with U

Graph 3: 
Os
p = 0.005
total length = [1, 2, 3, 4, 5] mm

Graph 4: 
Same but with U
'''

d_con = 0.01  # cm
d_bg_0 = 0.19  # cm
p_bg_0 = 1.0  # g/cc
p_con_0 = 0.005  # g/cc
p_vec = np.array([0.005, 0.003, 0.001, 0.0005, 0.0001])  # g/cc
d_tot_vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5]) - 0.01  # cm

# Graph One
Os = Material('Os', thickness=d_con, density=p_vec)
H2O = Material('H2O', thickness=d_bg_0, density=p_bg_0)
Os.match_energies_with(H2O)
plot_1d(bg=H2O, contrast=Os)
plt.ylim([0, 6])
plt.savefig('replicated_plots/fig_4A.png', dpi=300)

# Graph Two
U = Material('U', thickness=d_con, density=p_vec)
H2O = Material('H2O', thickness=d_bg_0, density=p_bg_0)
U.match_energies_with(H2O)
plot_1d(bg=H2O, contrast=U)
plt.ylim([0, 8])
plt.savefig('replicated_plots/fig_4B.png', dpi=300)

# Graph Three
Os = Material('Os', thickness=d_con, density=p_con_0)
H2O = Material('H2O', thickness=d_tot_vec, density=p_bg_0)
Os.match_energies_with(H2O)
plot_1d(bg=H2O, contrast=Os)
plt.ylim([0, 12])
plt.savefig('replicated_plots/fig_5A.png', dpi=300)

# Graph Three
U = Material('U', thickness=d_con, density=p_con_0)
H2O = Material('H2O', thickness=d_tot_vec, density=p_bg_0)
U.match_energies_with(H2O)
plot_1d(bg=H2O, contrast=U)
plt.ylim([0, 12])
plt.savefig('replicated_plots/fig_5B.png', dpi=300)
