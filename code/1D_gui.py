import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from misc_funcs import Material


def get_cnr(bg, contrast):
    CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
        np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                       contrast.u_p_int * contrast.density * contrast.thickness))
    return CNR


def update_text():
    ydata = cnr_line.get_ydata()
    ymax = ydata.max()
    Emax = bg.E_int[ydata == ymax]
    main_ax.text(0.8, 0.9, r'$E_{max}$' + ' = {}'.format(Emax),
                 transform=main_ax.transAxes,
                 bbox={'facecolor': 'white', 'edgecolor': 'black', 'pad'=10})


def update_y_axis():
    ydata = cnr_line.get_ydata()
    data_ymax = ydata.max()
    axis_ymax = main_ax.get_ylim()[-1]

    if data_ymax > axis_ymax:
        main_ax.set_ylim([0, data_ymax * 1.05])
    if data_ymax <= axis_ymax * 0.5:
        main_ax.set_ylim([0, data_ymax * 1.05])


def update(value):
    contrast.thickness = sl_contrast_thickness.val
    contrast.density = sl_contrast_density.val

    bg.thickness = sl_bg_thickness.val
    bg.density = sl_bg_density.val

    cnr_line.set_ydata(get_cnr(bg, contrast))
    update_y_axis()
    fig.canvas.draw_idle()


def update_mat(val):
    contrast.change_mat(bt_contrast_mat.value_selected)
    bg.change_mat(bt_bg_mat.value_selected)

    contrast.match_energies_with(bg)

    cnr_line.set_xdata(bg.E_int)
    cnr_line.set_ydata(get_cnr(bg, contrast))
    update_y_axis()

    fig.canvas.draw_idle()


def update_x_axis(val):
    main_ax.set_xlim([0, val])
    fig.canvas.draw_idle()


def reset(event):
    bt_bg_mat.set_active(0)
    sl_bg_thickness.reset()
    sl_bg_density.reset()
    bt_contrast_mat.set_active(1)
    sl_contrast_thickness.reset()
    sl_contrast_density.reset()
    sl_energy.reset()


# Initial values
bg = Material(name='H2O',
              thickness=0.2,
              density=1.0)

contrast = Material(name='Os',
                    thickness=0.01,
                    density=0.003)

contrast.match_energies_with(bg)


# Figure properties
fig, main_ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(left=0.36, bottom=0.1, top=0.9)
fig.suptitle('MicroCT CNR Calculator')
fig.set_facecolor('lightgray')

# Graph properties
cnr_line, = main_ax.plot(bg.E_int, get_cnr(bg, contrast), 'k')
update_text()
main_ax.set_xlabel('E [keV]')
main_ax.set_ylabel('CNR')
main_ax.set_title('Contrast to Noise Ratio (CNR)')
main_ax.set_xlim([0, 50])
main_ax.grid(True)


# Choose Contrast Material
ax_contrast_mat = plt.axes([0.07, 0.65, 0.08, 0.25], aspect='equal')
ax_contrast_mat.set_title('Contrast\n Material')
bt_contrast_mat = RadioButtons(
    ax_contrast_mat, ('H2O', 'Os', 'U', 'Pb'), active=1)
bt_contrast_mat.on_clicked(update_mat)

# Choose Background Material
ax_bg_mat = plt.axes([0.20, 0.65, 0.08, 0.25], aspect='equal')
ax_bg_mat.set_title('Background\n Material')
bt_bg_mat = RadioButtons(
    ax_bg_mat, ('H2O', 'Os', 'U', 'Pb'), active=0)
bt_bg_mat.on_clicked(update_mat)

# Choose Contrast Thickness
d_c_min = 0.01
d_c_max = 2
ax_contrast_thickness = plt.axes([0.07, 0.6, 0.21, 0.03])
ax_contrast_thickness.set_title('Contrast Parameters')
sl_contrast_thickness = Slider(
    ax_contrast_thickness, r'$d_{con}$', d_c_min, d_c_max, valinit=contrast.thickness)
sl_contrast_thickness.on_changed(update)

# Choose Contrast Density
p_c_min = 0.0005
p_c_max = 0.005
ax_contrast_density = plt.axes([0.07, 0.55, 0.21, 0.03])
sl_contrast_density = Slider(
    ax_contrast_density, r'$\rho_{con}$ g/cc', p_c_min, p_c_max, valinit=contrast.density, valfmt='%1.4f')
sl_contrast_density.on_changed(update)

# Choose Total Thickness
d_bg_min = 0.01
d_bg_max = 2
ax_bg_thickness = plt.axes([0.07, 0.40, 0.21, 0.03])
ax_bg_thickness.set_title('Background Parameters')
sl_bg_thickness = Slider(
    ax_bg_thickness, r'$d_{tot}$', d_bg_min, d_bg_max, valinit=bg.thickness)
sl_bg_thickness.on_changed(update)

# Choose Background Density
p_bg_min = 0.5
p_bg_max = 1.5
ax_bg_density = plt.axes([0.07, 0.35, 0.21, 0.03])
sl_bg_density = Slider(
    ax_bg_density, r'$\rho_{bg}$', p_bg_min, p_bg_max, valinit=bg.density, valfmt='%1.4f')
sl_bg_density.on_changed(update)

# Choose Maximum Energy
E_min = 0
E_max = 100
ax_energy = plt.axes([0.07, 0.20, 0.21, 0.03])
sl_energy = Slider(
    ax_energy, r'$E_{max}$', E_min, E_max, valinit=50, valfmt='%1.0f')
ax_energy.set_title('Maximum Energy')
sl_energy.on_changed(update_x_axis)

# Reset Defaults
reset_ax = plt.axes([0.12, 0.10, 0.1, 0.05])
reset_button = Button(reset_ax, 'Reset Defaults')
reset_button.on_clicked(reset)

plt.show(block=False)
