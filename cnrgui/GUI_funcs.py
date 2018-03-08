#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from material import Material


class Material_Widget(object):
    '''
    Contains parameters affecting the layout and function of radio buttons
    used to choose different background and contrast materials.
    '''

    def __init__(self, rect, title, default, update_func):
        self.ax = plt.axes(rect, aspect='equal')
        self.ax.set_title(title)
        self.button = RadioButtons(
            self.ax, ('H2O', 'Os', 'U', 'Pb'), active=default)
        self.button.on_clicked(update_func)


class Parameter_Widget(object):
    '''
    Contains parameters affecting the layout and function of sliders used to
    control all physical experimental parameters.
    '''

    def __init__(self, rect, title, low, high, init, units, update_func, sup_title=None, fmt='% 1.4f'):
        self.ax = plt.axes(rect)
        self.high = high
        if sup_title is not None:
            self.ax.set_title(sup_title)
        self.slider = Slider(self.ax, title, low,
                             high, valinit=init, valfmt=fmt + ' ' + units)
        self.slider.on_changed(update_func)


class GUI(object):
    '''
    Creates a new GUI updating a curve of CNR vs energy for a
    given a set of input parameters

    Parameters
    __________
    thickness_values : ndarray
        Min and max values for the thickness sliders. In the format:
        np.array([min_thickness, max_thickness])
    bg_density_values : ndarray
        Min and max values for the background density slider
    contrast_density_values : ndarray
        Min and max values for the contrast material density slider
    max_intensity_value : int
        Maximum number of photons for entrance intensity slider
    thickness_units : str
        Either 'mm' or 'nm'
    bg, contrast : int
        Choice of initial materials.
             0 - H2O
             1 - Os
             2 - U
             3 - Pb
    init_max_E : int
        Initial value for maximum displayed energy value
    figsize : tuple
        Sets the dimensions of the GUI figure
    linecolor : str
        Sets the color of the CNR line plot. Choose from matplotlib keywords


    '''

    def __init__(self, thickness_values, bg_density_values, contrast_density_values,
                 max_intensity_value, thickness_units='mm', bg=0, contrast=1, init_max_E=40,
                 figsize=(14, 8), linecolor='k'):

        mat_names = ['H2O', 'Os', 'U', 'Pb']

        self.nm = False if thickness_units == 'mm' else True

        # Initial values
        self.bg = Material(name=mat_names[bg],
                           thickness=thickness_values.mean() * 3 / 4,
                           density=bg_density_values.mean())

        self.contrast = Material(name=mat_names[contrast],
                                 thickness=thickness_values.mean() / 4,
                                 density=contrast_density_values.mean())

        self.contrast.match_energies_with(self.bg)

        # Figure properties
        self.fig, self.main_ax = plt.subplots(figsize=figsize)
        plt.subplots_adjust(left=0.40, bottom=0.1, top=0.9, right=0.93)
        self.fig.canvas.set_window_title('MicroCT CNR Calculator')
        self.fig.set_facecolor('lightgray')

        # Default Main Axes properties
        self.cnr_line, = self.main_ax.plot(
            self.bg.E_int, self.get_cnr(self.bg, self.contrast), linecolor)
        self.main_ax.set_xlabel('E [keV]')
        self.main_ax.set_ylabel('CNR')
        eqn_abs = r'CNR = $\sqrt{I_0}\left(\frac{\mu}{\rho}\right)_{c}(E)\rho_{c}$ / '
        eqn_exp = r'$\sqrt{exp\{\left(\frac{\mu}{\rho}\right)_{bg}(E)\rho_{bg} d_{tot}\} + exp\{\left(\frac{\mu}{\rho}\right)_{c}(E)\rho_c d_c + \left(\frac{\mu}{\rho}\right)_{bg}(E)\rho_{bg}d_{tot}\}}$'
        self.main_ax.set_title(eqn_abs + eqn_exp)
        self.main_ax.set_xlim([0, init_max_E])
        self.main_ax.grid(True)

        # Material selection

        self.contrast_mat_widget = Material_Widget(rect=[0.07, 0.70, 0.08, 0.25],
                                                   title='Contrast\n Material',
                                                   default=contrast,  # Default: Osmium
                                                   update_func=self.update_mat)

        self.bg_mat_widget = Material_Widget(rect=[0.20, 0.70, 0.08, 0.25],
                                             title='Background\n Material',
                                             default=bg,  # Default: H2O
                                             update_func=self.update_mat)

        # Background parameters

        self.bg_thickness_widget = Parameter_Widget(rect=[0.07, 0.65, 0.21, 0.03],
                                                    title=r'$d_{tot}$',
                                                    low=thickness_values[0],
                                                    high=thickness_values[1],
                                                    init=self.bg.thickness,
                                                    units='nm' if self.nm else 'mm',
                                                    fmt='%1.0f' if self.nm else '%1.2f',
                                                    sup_title='Background Parameters',
                                                    update_func=self.update)

        self.bg_density_widget = Parameter_Widget(rect=[0.07, 0.60, 0.21, 0.03],
                                                  title=r'$\rho_{bg}$',
                                                  low=bg_density_values[0],
                                                  high=bg_density_values[1],
                                                  init=self.bg.density,
                                                  fmt='%1.2f',
                                                  units='g/cc',
                                                  update_func=self.update)

        # Contrast Parameters

        self.contrast_thickness_widget = Parameter_Widget(rect=[0.07, 0.50, 0.21, 0.03],
                                                          title=r'$d_{con}$',
                                                          low=thickness_values[0],
                                                          high=thickness_values[1],
                                                          init=self.contrast.thickness,
                                                          units='nm' if self.nm else 'mm',
                                                          fmt='%1.0f' if self.nm else '%1.2f',
                                                          sup_title='Contrast Parameters',
                                                          update_func=self.update)

        self.contrast_density_widget = Parameter_Widget(rect=[0.07, 0.45, 0.21, 0.03],
                                                        title=r'$\rho_{con}$',
                                                        low=contrast_density_values[0],
                                                        high=contrast_density_values[1],
                                                        init=self.contrast.density,
                                                        units='g/cc',
                                                        update_func=self.update)

        # System parameters

        self.intensity_widget = Parameter_Widget(rect=[0.07, 0.35, 0.21, 0.03],
                                                 title=r'$I_0$',
                                                 low=1,
                                                 high=max_intensity_value,
                                                 init=1,
                                                 units='photons',
                                                 fmt='%1.0f',
                                                 sup_title='Entrance Intensity',
                                                 update_func=self.update)

        self.low_energy_widget = Parameter_Widget(rect=[0.07, 0.25, 0.21, 0.03],
                                                  title=r'$E_{min}$',
                                                  low=0,
                                                  high=100,
                                                  init=0,
                                                  fmt='%1.1f',
                                                  sup_title='Energy',
                                                  units='keV',
                                                  update_func=self.update_x_axis)

        self.high_energy_widget = Parameter_Widget(rect=[0.07, 0.20, 0.21, 0.03],
                                                   title=r'$E_{max}$',
                                                   low=0,
                                                   high=100,
                                                   init=40,
                                                   fmt='%1.1f',
                                                   units='keV',
                                                   update_func=self.update_x_axis)

        # Show Optimal Energy
        ax_opt_energy_button = plt.axes([0.07, 0.12, 0.15, 0.03])
        ax_opt_energy_value = plt.axes([0.23, 0.12, 0.06, 0.03])
        ax_opt_energy_value.set_xticks([])
        ax_opt_energy_value.set_yticks([])
        self.E_opt_text = ax_opt_energy_value.text(0.1, 0.35, '')
        button_opt_energy = Button(
            ax_opt_energy_button, 'Calculate optimal energy')
        button_opt_energy.on_clicked(self.get_optimal_energy)

        # Reset Defaults
        reset_ax = plt.axes([0.07, 0.05, 0.1, 0.05])
        button_reset = Button(reset_ax, 'Reset Defaults')
        button_reset.on_clicked(self.reset)

        plt.show(block=True)

    def get_cnr(self, bg, contrast, I=1):
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
                     thickness : mm (or nm if nm=True)


        Returns
        _______
        CNR : ndarray
            Values of CNR at the energy values given by the E_int attribute of both
            bg and contrast
        '''

        # Sets conversion factor from input thickness unit to cm
        if self.nm:
            conv = 1e-7
        else:
            conv = 0.1

        # CNR = np.sqrt(I) * abs(contrast.u_p_int * contrast.density) * \
        #     np.sqrt(np.exp(-bg.u_p_int * bg.density * (bg.thickness * conv) -
        # contrast.u_p_int * contrast.density * (contrast.thickness * conv)))

        with np.errstate(over='ignore'):
            CNR = np.sqrt(I) * contrast.u_p_int * \
                contrast.density / np.sqrt(np.exp(bg.u_p_int * bg.density * (bg.thickness * conv)) +
                                           np.exp(contrast.u_p_int * contrast.density * (contrast.thickness * conv) +
                                                  bg.u_p_int * bg.density * (bg.thickness * conv)))

        return CNR

    def update(self, value):
        '''
        Primary function for updating the CNR curve in response to new parameter
        values from the sliders. Controls for physically impossible combinations of
        parameters.
        '''

        # In the case that the background thickness is set to be smaller than the
        # contrast thickness, this sets them to be equal. This way, it updates
        # both thicknesses in real time as the user slides the total thickness
        # lower than the contrast thickness.
        if self.bg_thickness_widget.slider.val < self.contrast_thickness_widget.slider.val:
            # self.bg.thickness = self.contrast_thickness_widget.slider.val
            self.contrast_thickness_widget.slider.set_val(
                self.bg_thickness_widget.slider.val)

        else:
            self.bg.thickness = self.bg_thickness_widget.slider.val

            # Along the same lines, this limits the contrast thickness slider to be
            # no greater than the current value of the total thickness slider.
            self.contrast_thickness_widget.slider.valmax = self.bg_thickness_widget.slider.val

        # Refreshes all other parameters
        self.bg.density = self.bg_density_widget.slider.val
        self.contrast.thickness = self.contrast_thickness_widget.slider.val
        self.contrast.density = self.contrast_density_widget.slider.val
        intensity = self.intensity_widget.slider.val

        try:
            # Recalculates CNR
            self.cnr_line.set_ydata(self.get_cnr(
                self.bg, self.contrast, intensity))
            self.update_y_axis()  # Updates y-axis limits
            # Resests optimal energy display to blank
            self.E_opt_text.set_text('')
            self.fig.canvas.draw_idle()  # Redraws curve
        except ValueError:
            # Things blow up when the thicknesses are equal
            pass

    def update_mat(self, val):
        '''
        Updates the background and contrast materials in response to a new
        selection by the user.
        '''

        # Updates name, E and u_p attributes of materials, keeps other parameters
        # fixed
        self.contrast.change_mat(
            self.contrast_mat_widget.button.value_selected)
        self.bg.change_mat(self.bg_mat_widget.button.value_selected)

        # Re-syncs materials' energy values
        self.contrast.match_energies_with(self.bg)

        # Resets plotted data
        self.cnr_line.set_xdata(self.bg.E_int)
        self.cnr_line.set_ydata(self.get_cnr(self.bg, self.contrast))
        self.update_y_axis()
        self.E_opt_text.set_text('')

        self.fig.canvas.draw_idle()

    def update_y_axis(self):
        '''
        Updates the CNR axis limits so that the curve is fully contained in the axes.

        Conditions:
        1) If the maximum CNR exceeds the upper limit of the y-axis,
           the upper limit is increased by 5%
        2) If the maximum CNR is lower than 15% of the upper limit of the y-axis,
           the upper limit is set to 5% greater than the maximum CNR.
        '''
        ydata = self.cnr_line.get_ydata()
        data_ymax = ydata.max()
        axis_ymax = self.main_ax.get_ylim()[-1]

        if data_ymax > axis_ymax:
            self.main_ax.set_ylim([0, data_ymax * 1.05])
        if data_ymax <= axis_ymax * 0.15:
            self.main_ax.set_ylim([0, data_ymax * 1.05])

    def update_x_axis(self, val):
        '''
        Resets the maximum energy axis value in response to change in slider.
        '''

        E_max = self.high_energy_widget.slider.val
        E_min = self.low_energy_widget.slider.val
        width = 0.5

        self.high_energy_widget.slider.valmin = E_min + width
        self.low_energy_widget.slider.valmax = E_max - width

        self.main_ax.set_xlim(
            [self.low_energy_widget.slider.val, self.high_energy_widget.slider.val])

        self.E_opt_text.set_text('')
        self.fig.canvas.draw_idle()

    def get_optimal_energy(self, val):
        '''
        Retrieves the maximum CNR value from the current curve and displays it in
        the designated text box.
        '''

        E_low, E_high = self.main_ax.get_xlim()
        ydata = self.cnr_line.get_ydata()
        xdata = self.cnr_line.get_xdata()

        ymax = ydata[(xdata >= E_low) & (xdata <= E_high)].max()
        Emax = xdata[ydata == ymax][0]
        self.E_opt_text.set_text('{} keV'.format(np.round(Emax, 2)))
        self.fig.canvas.draw_idle()

    def reset(self, event):
        '''
        Resets all parameters to defaults.
        '''
        self.bg_mat_widget.button.set_active(0)
        self.bg_thickness_widget.slider.reset()
        self.bg_density_widget.slider.reset()
        self.contrast_mat_widget.button.set_active(1)
        self.contrast_thickness_widget.slider.reset()
        self.contrast_density_widget.slider.reset()
        self.low_energy_widget.slider.reset()
        self.high_energy_widget.slider.reset()
        self.intensity_widget.slider.reset()
