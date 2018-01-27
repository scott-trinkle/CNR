import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from misc_funcs import Material


def get_cnr(bg, contrast):
    CNR = abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
        np.sqrt(np.exp(-bg.u_p_int * bg.density * bg.thickness -
                       contrast.u_p_int * contrast.density * contrast.thickness))
    return CNR


def get_optimal_energy(val):
    ydata = cnr_line.get_ydata()
    ymax = ydata.max()
    Emax = bg.E_int[ydata == ymax][0]
    E_opt_text.set_text('{} keV'.format(np.round(Emax, 2)))
    fig.canvas.draw_idle()


def update_y_axis():
    ydata = cnr_line.get_ydata()
    data_ymax = ydata.max()
    axis_ymax = main_ax.get_ylim()[-1]

    if data_ymax > axis_ymax:
        main_ax.set_ylim([0, data_ymax * 1.05])
    if data_ymax <= axis_ymax * 0.15:
        main_ax.set_ylim([0, data_ymax * 1.05])


def update(value):

    if total_thickness_widget.slider.val < contrast_thickness_widget.slider.val:
        bg.thickness = 0
        contrast_thickness_widget.slider.set_val(
            total_thickness_widget.slider.val)

    else:
        bg.thickness = total_thickness_widget.slider.val - contrast.thickness
        contrast_thickness_widget.slider.valmax = total_thickness_widget.slider.val

    bg.density = bg_density_widget.slider.val

    contrast.thickness = contrast_thickness_widget.slider.val
    contrast.density = contrast_density_widget.slider.val

    try:
        cnr_line.set_ydata(get_cnr(bg, contrast))
        update_y_axis()
        E_opt_text.set_text('')
        fig.canvas.draw_idle()
    except ValueError:
        pass


def update_mat(val):
    contrast.change_mat(contrast_mat_widget.button.value_selected)
    bg.change_mat(bg_mat_widget.button.value_selected)

    contrast.match_energies_with(bg)

    cnr_line.set_xdata(bg.E_int)
    cnr_line.set_ydata(get_cnr(bg, contrast))
    update_y_axis()
    E_opt_text.set_text('')

    fig.canvas.draw_idle()


def update_x_axis(val):
    main_ax.set_xlim([0, val])
    fig.canvas.draw_idle()


def reset(event):
    bg_mat_widget.button.set_active(0)
    total_thickness_widget.slider.reset()
    bg_density_widget.slider.reset()
    contrast_mat_widget.button.set_active(1)
    contrast_thickness_widget.slider.reset()
    contrast_density_widget.slider.reset()
    energy_widget.slider.reset()


class Material_Widget(object):
    def __init__(self, rect, title, default):
        self.ax = plt.axes(rect, aspect='equal')
        self.ax.set_title(title)
        self.button = RadioButtons(
            self.ax, ('H2O', 'Os', 'U', 'Pb'), active=default)
        self.button.on_clicked(update_mat)


class Parameter_Widget(object):
    def __init__(self, rect, title, low, high, init, units, sup_title=None, fmt='%1.4f', update_func=update):
        self.ax = plt.axes(rect)
        if sup_title is not None:
            self.ax.set_title(sup_title)
        self.slider = Slider(self.ax, title, low,
                             high, valinit=init, valfmt=fmt + ' ' + units)
        self.slider.on_changed(update_func)


# Initial values
bg = Material(name='H2O',
              thickness=0.19,
              density=1.0)

contrast = Material(name='Os',
                    thickness=0.01,
                    density=0.003)

contrast.match_energies_with(bg)


# Figure properties
fig, main_ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(left=0.40, bottom=0.1, top=0.9, right=0.93)
fig.canvas.set_window_title('MicroCT CNR Calculator')
fig.set_facecolor('lightgray')

# Main Axes properties
cnr_line, = main_ax.plot(bg.E_int, get_cnr(bg, contrast), 'k')
main_ax.set_xlabel('E [keV]')
main_ax.set_ylabel('CNR')
main_ax.set_title('Contrast to Noise Ratio (CNR)')
main_ax.set_xlim([0, 50])
main_ax.grid(True)


# Widget initiation
contrast_mat_widget = Material_Widget(rect=[0.07, 0.65, 0.08, 0.25],
                                      title='Contrast\n Material',
                                      default=1)

bg_mat_widget = Material_Widget(rect=[0.20, 0.65, 0.08, 0.25],
                                title='Background\n Material',
                                default=0)


total_thickness_widget = Parameter_Widget(rect=[0.07, 0.60, 0.21, 0.03],
                                          title=r'$d_{tot}$',
                                          low=0.01,
                                          high=2,
                                          init=bg.thickness + contrast.thickness,
                                          units='cm',
                                          sup_title='Background Parameters')

bg_density_widget = Parameter_Widget(rect=[0.07, 0.55, 0.21, 0.03],
                                     title=r'$\rho_{bg}$',
                                     low=0.5,
                                     high=1.5,
                                     init=bg.density,
                                     units='g/cc')

contrast_thickness_widget = Parameter_Widget(rect=[0.07, 0.4, 0.21, 0.03],
                                             title=r'$d_{con}$',
                                             low=0.01,
                                             high=2,
                                             init=contrast.thickness,
                                             units='cm',
                                             sup_title='Contrast Parameters')

contrast_density_widget = Parameter_Widget(rect=[0.07, 0.35, 0.21, 0.03],
                                           title=r'$\rho_{con}$',
                                           low=0.0005,
                                           high=0.005,
                                           init=contrast.density,
                                           units='g/cc')

energy_widget = Parameter_Widget(rect=[0.07, 0.20, 0.21, 0.03],
                                 title=r'$E_{max}$',
                                 low=0,
                                 high=100,
                                 init=50,
                                 fmt='%1.0f',
                                 sup_title='Maximum Energy',
                                 units='keV',
                                 update_func=update_x_axis)


# Show Optimal Energy
ax_opt_energy_button = plt.axes([0.07, 0.12, 0.13, 0.03])
ax_opt_energy_value = plt.axes([0.23, 0.12, 0.06, 0.03])
ax_opt_energy_value.set_xticks([])
ax_opt_energy_value.set_yticks([])

E_opt_text = ax_opt_energy_value.text(0.1, 0.35, '')

button_opt_energy = Button(ax_opt_energy_button, 'Display optimal energy')
button_opt_energy.on_clicked(get_optimal_energy)


# Reset Defaults
reset_ax = plt.axes([0.07, 0.05, 0.1, 0.05])
button_reset = Button(reset_ax, 'Reset Defaults')
button_reset.on_clicked(reset)


plt.show(block=True)
