import numpy as np
from material import Material
import matplotlib.pyplot as plt

Os = Material(name='Os',
              thickness=0.01)  # cmn

H2O = Material(name='H2O',
               thickness=0.19,  # cm
               density=1.0)

Os.match_energies_with(H2O)


ind = 500


def diff(p, bg=H2O, c=Os, ind=ind):
    return abs(c.u_p_int[ind] * p - bg.u_p_int[ind] * bg.density)


p = np.linspace(0.0001, 0.1)

for i in [530, 550, 565]:
    plt.plot(p, diff(p, ind=i), label='E = {} keV'.format(
        np.round(Os.E_int[i], 2)))

plt.legend()
plt.title(r'$|(\mu/\rho)_c(E)\rho_c - (\mu/\rho)_{bg}(E)\rho_{bg}|$')
plt.xlabel(r'$\rho_c$' + '[g/cc]')
plt.savefig('diff_vs_rho.png', dpi=300)
