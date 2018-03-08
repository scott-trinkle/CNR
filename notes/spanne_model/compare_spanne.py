import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('../../cnrgui')
from material import Material


H2O = Material('H2O',
               thickness=2,
               density=1)

Os = Material('Os',
              thickness=0.1,
              density=0.0005)

H2O.match_energies_with(Os)


def get_cnr(bg, contrast, I=1, method='spanne'):
    conv = 0.1

    if method == 'spanne':
        CNR = np.sqrt(I) * abs(contrast.u_p_int * contrast.density) / np.sqrt(np.exp(bg.u_p_int * bg.density * (bg.thickness * conv)) +
                                                                              np.exp(contrast.u_p_int * contrast.density * (contrast.thickness * conv) + bg.u_p_int * bg.density * (bg.thickness * conv)))
    elif method == 'ours':
        CNR = np.sqrt(I) * abs(contrast.u_p_int * contrast.density) * \
            np.sqrt(np.exp(-bg.u_p_int * bg.density * (bg.thickness * conv) -
                           contrast.u_p_int * contrast.density * (contrast.thickness * conv)))

    return CNR


colors = ['C0', 'C1', 'C2']

plt.figure(figsize=(12, 8))

for i, p in enumerate([0.002, 0.001, 0.0005]):
    Os.density = p
    CNR_s = get_cnr(H2O, Os)
    CNR_o = get_cnr(H2O, Os, method='ours')

    plt.plot(Os.E_int, CNR_s, color=colors[i],
             ls=':', label=r'Spanne: $\rho_c$ = {}'.format(p))
    plt.plot(Os.E_int, CNR_o, color=colors[i],
             label=r'Current: $\rho_c$ = {}'.format(p))

plt.xlabel('E [keV]')
plt.ylabel('CNR')
plt.title('Comparison of CNR models, Os contrast on H2O background')
plt.legend()
plt.tight_layout()
plt.savefig('../notes/spanne_model/comparison.png', dpi=300)
