from cnrgui.material import Material
from cnrgui.util import cnr, match_energies
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib.ticker import MaxNLocator


# Initializing materials
H2O = Material('H2O',
               thickness=2,
               density=1)
Os = Material('Os',
              thickness=0.1,
              density=0.05)
# Os.match_energies_with(H2O)
match_energies(H2O, Os)

with plt.style.context('seaborn-deep'):
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

ax_ins = inset_axes(axes[0], width='40%', height='45%', loc=9)

for i, bw in enumerate([0, 1e-2, 1e-4]):
    axes[0].plot(H2O.E, cnr(H2O, Os, bw=bw),
                 color='C{}'.format(i), label='BW={:.0e}'.format(bw))
    ax_ins.plot(H2O.E, cnr(H2O, Os, bw=bw),
                color='C{}'.format(i), label='BW={}'.format(bw))

x1, x2 = 12.44, 12.47
y1, y2 = 5.32, 5.335
ax_ins.set_xlim(x1, x2)
ax_ins.set_ylim(y1, y2)
ax_ins.xaxis.set_major_locator(MaxNLocator(4))
ax_ins.yaxis.set_major_locator(MaxNLocator(4))
ax_ins.ticklabel_format(useOffset=False)
mark_inset(axes[0], ax_ins, loc1=2, loc2=3, fc='none', ec='0.5')

axes[0].set_title('H$_2$O ({} mm, {} g/cc) and Os: ({} mm, {} g/cc), $I_0$ = 1'.format(H2O.thickness,
                                                                                       H2O.density,
                                                                                       Os.thickness,
                                                                                       Os.density))
axes[0].set_ylabel('CNR')
axes[0].legend()
axes[0].grid(True)

cnr0 = cnr(H2O, Os, bw=0)

for i, bw in enumerate([1e-2, 1e-4]):
    cnrbw = cnr(H2O, Os, bw=bw)
    with np.errstate(invalid='ignore'):
        diff = np.where(cnr0 != 0, abs(cnrbw - cnr0) / cnr0 * 100, 0)
    axes[1].semilogy(H2O.E, diff, ':.', label='BW={:.0e}'.format(bw),
                     color='C{}'.format(i+1))

axes[1].grid(True)
axes[1].set_xlabel('Energy [keV]')
axes[1].set_ylabel(r'|CNR$_{BW}$ - CNR$_{0}$| / CNR$_{0}$ * 100')

plt.tight_layout()
plt.savefig('report/cnrwithbw.pdf')
