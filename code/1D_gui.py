#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from misc_funcs import Material
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

##########################################################################
#                                Functions                               #
##########################################################################


def get_cnr(bg, contrast, I=1):
    ''' 
    Calculates 1D CNR for two-material model. 

    Parameters
    __________
    bg : Material
        Background material object with given thickness, density
    contrast: Material
        Contrast material object with given thickness, density
    I : int
        Entrance intensity (number of photons)

    NOTES: 
    (1) bg and contrast should already have matched E vectors using the 
        match_energies_with method
    (2) Assumes the following parameter units:

                         I : photons
                       u_p : cm2/g
                   density : g / cm3
                 thickness : mm 


    Returns
    _______
    CNR : ndarray
        Values of CNR at the energy values given by the E_int attribute of both 
        bg and contrast
    '''

    CNR = np.sqrt(I) * abs(bg.u_p_int * bg.density - contrast.u_p_int * contrast.density) * \
        np.sqrt(np.exp(-bg.u_p_int * bg.density * (bg.thickness * 0.1) -
                       contrast.u_p_int * contrast.density * (contrast.thickness * 0.1)))
    return CNR


def update(value):
    '''
    Primary function for updating the CNR curve in response to new parameter
    values from the sliders. Controls for physically impossible combinations of
    parameters. 
    '''

    # In the case that the total thickness is set to be smaller than the
    # contrast thickness, this sets the background thickness to 0 and the
    # contrast thickness equal to the total thickness. This way, it updates
    # both total and contrast thicknesses in real time as the user slides the
    # total thickness lower than the contrast thickness.
    if total_thickness_widget.slider.val < contrast_thickness_widget.slider.val:
        bg.thickness = 0
        contrast_thickness_widget.slider.set_val(
            total_thickness_widget.slider.val)

    else:
        bg.thickness = total_thickness_widget.slider.val - contrast.thickness

        # Along the same lines, this limits the contrast thickness slider to be
        # no greater than the current value of the total thickness slider.
        contrast_thickness_widget.slider.valmax = total_thickness_widget.slider.val

    # Refreshes all other parameters
    bg.density = bg_density_widget.slider.val
    contrast.thickness = contrast_thickness_widget.slider.val
    contrast.density = contrast_density_widget.slider.val
    intensity = intensity_widget.slider.val

    try:
        # Recalculates CNR
        cnr_line.set_ydata(get_cnr(bg, contrast, intensity))
        update_y_axis()  # Updates y-axis limits
        E_opt_text.set_text('')  # Resests optimal energy display to blank
        fig.canvas.draw_idle()  # Redraws curve
    except ValueError:
        # Things blow up when the background thickness is 0.
        pass


def update_mat(val):
    '''
    Updates the background and contrast materials in response to a new 
    selection by the user. 
    '''

    # Updates name, E and u_p attributes of materials, keeps other parameters
    # fixed
    contrast.change_mat(contrast_mat_widget.button.value_selected)
    bg.change_mat(bg_mat_widget.button.value_selected)

    # Re-syncs materials' energy values
    contrast.match_energies_with(bg)

    # Resets plotted data
    cnr_line.set_xdata(bg.E_int)
    cnr_line.set_ydata(get_cnr(bg, contrast))
    update_y_axis()
    E_opt_text.set_text('')

    fig.canvas.draw_idle()


def update_y_axis():
    '''
    Updates the CNR axis limits so that the curve is fully contained in the axes. 

    Conditions:
    1) If the maximum CNR exceeds the upper limit of the y-axis, 
       the upper limit is increased by 5%
    2) If the maximum CNR is lower than 15% of the upper limit of the y-axis, 
       the upper limit is set to 5% greater than the maximum CNR. 
    '''
    ydata = cnr_line.get_ydata()
    data_ymax = ydata.max()
    axis_ymax = main_ax.get_ylim()[-1]

    if data_ymax > axis_ymax:
        main_ax.set_ylim([0, data_ymax * 1.05])
    if data_ymax <= axis_ymax * 0.15:
        main_ax.set_ylim([0, data_ymax * 1.05])


def update_x_axis(val):
    '''
    Resets the maximum energy axis value in response to change in slider. 
    '''
    main_ax.set_xlim([0, val])
    fig.canvas.draw_idle()


def get_optimal_energy(val):
    '''
    Retrieves the maximum CNR value from the current curve and displays it in 
    the designated text box. 
    '''
    ydata = cnr_line.get_ydata()
    ymax = ydata.max()
    Emax = bg.E_int[ydata == ymax][0]
    E_opt_text.set_text('{} keV'.format(np.round(Emax, 2)))
    fig.canvas.draw_idle()


def reset(event):
    '''
    Resets all parameters to defaults.
    '''
    bg_mat_widget.button.set_active(0)
    total_thickness_widget.slider.reset()
    bg_density_widget.slider.reset()
    contrast_mat_widget.button.set_active(1)
    contrast_thickness_widget.slider.reset()
    contrast_density_widget.slider.reset()
    energy_widget.slider.reset()
    intensity_widget.slider.reset()


##########################################################################
#                                Classes                                 #
##########################################################################


class Material_Widget(object):
    '''
    Contains parameters affecting the layout and function of radio buttons
    used to choose different background and contrast materials. 
    '''

    def __init__(self, rect, title, default):
        self.ax = plt.axes(rect, aspect='equal')
        self.ax.set_title(title)
        self.button = RadioButtons(
            self.ax, ('H2O', 'Os', 'U', 'Pb'), active=default)
        self.button.on_clicked(update_mat)


class Parameter_Widget(object):
    '''
    Contains parameters affecting the layout and function of sliders used to 
    control all physical experimental parameters. 
    '''

    def __init__(self, rect, title, low, high, init, units, sup_title=None, fmt='%1.4f', update_func=update):
        self.ax = plt.axes(rect)
        if sup_title is not None:
            self.ax.set_title(sup_title)
        self.slider = Slider(self.ax, title, low,
                             high, valinit=init, valfmt=fmt + ' ' + units)
        self.slider.on_changed(update_func)

##########################################################################
#                          Initial Values                                #
##########################################################################



# Initial values
bg = Material(name='H2O',
              thickness=1.9,  # mm
              density=1.0)  # g/cc

contrast = Material(name='Os',
                    thickness=0.1,  # mm
                    density=0.003)  # g/cc

contrast.match_energies_with(bg)


# Figure properties
fig, main_ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(left=0.40, bottom=0.1, top=0.9, right=0.93)
fig.canvas.set_window_title('MicroCT CNR Calculator')
fig.set_facecolor('lightgray')

# Default Main Axes properties
cnr_line, = main_ax.plot(bg.E_int, get_cnr(bg, contrast), 'k')
main_ax.set_xlabel('E [keV]')
main_ax.set_ylabel('CNR')
eqn_abs = r'CNR = $\sqrt{I_0}|(\frac{\mu}{\rho})_{c}(E)\rho_{c} - (\frac{\mu}{\rho})_{bg}(E)\rho_{bg}|$ * '
eqn_exp = r'$\sqrt{exp\{-(\frac{\mu}{\rho})_{c}(E)\rho_c d_c -(\frac{\mu}{\rho})_{bg}(E)\rho_{bg}d_{bg}\}}$'
main_ax.set_title(eqn_abs + eqn_exp)
main_ax.set_xlim([0, 40])
main_ax.grid(True)


##########################################################################
#                              Widgets                                   #
##########################################################################


# Material selection

contrast_mat_widget = Material_Widget(rect=[0.07, 0.65, 0.08, 0.25],
                                      title='Contrast\n Material',
                                      default=1)  # Default: Osmium

bg_mat_widget = Material_Widget(rect=[0.20, 0.65, 0.08, 0.25],
                                title='Background\n Material',
                                default=0)  # Default: H2O

# Background parameters

total_thickness_widget = Parameter_Widget(rect=[0.07, 0.60, 0.21, 0.03],
                                          title=r'$d_{tot}$',
                                          low=0.01,
                                          high=10,
                                          init=bg.thickness + contrast.thickness,
                                          units='mm',
                                          fmt='%1.2f',
                                          sup_title='Background Parameters')

bg_density_widget = Parameter_Widget(rect=[0.07, 0.55, 0.21, 0.03],
                                     title=r'$\rho_{bg}$',
                                     low=0.5,
                                     high=1.5,
                                     init=bg.density,
                                     fmt='%1.2f',
                                     units='g/cc')

# Contrast Parameters

contrast_thickness_widget = Parameter_Widget(rect=[0.07, 0.45, 0.21, 0.03],
                                             title=r'$d_{con}$',
                                             low=0.01,
                                             high=10,
                                             init=contrast.thickness,
                                             units='mm',
                                             fmt='%1.2f',
                                             sup_title='Contrast Parameters')

contrast_density_widget = Parameter_Widget(rect=[0.07, 0.40, 0.21, 0.03],
                                           title=r'$\rho_{con}$',
                                           low=0.0001,
                                           high=0.05,
                                           init=contrast.density,
                                           units='g/cc')

# System parameters

intensity_widget = Parameter_Widget(rect=[0.07, 0.30, 0.21, 0.03],
                                    title=r'$I_0$',
                                    low=1,
                                    high=1e5,
                                    init=1,
                                    units='photons',
                                    fmt='%1.0f',
                                    sup_title='Entrance Intensity')

energy_widget = Parameter_Widget(rect=[0.07, 0.20, 0.21, 0.03],
                                 title=r'$E_{max}$',
                                 low=0,
                                 high=100,
                                 init=40,
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
