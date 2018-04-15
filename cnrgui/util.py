import numpy as np
from scipy.interpolate import interp1d


def log_interp(xx, yy, xx_new):
    '''
    Import model input, model output, new input, returns log-interpolated
    output
    '''

    logx = np.log10(xx)
    logy = np.log10(yy)
    lin_interp = interp1d(logx, logy)

    def log_interp(zz): return np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp(xx_new)


def cnr(bg, contrast, I0=1, bw=1e-2, conv=0.1, truncate=4, n=50):
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

    E_vals = bg.E_int

    u_c = contrast.u_p_int * contrast.density
    d_c = contrast.thickness * conv
    u_bg = bg.u_p_int * bg.density
    d_bg = bg.thickness * conv

    A1 = u_bg * d_bg
    A2 = u_bg * d_bg + u_c * d_c

    N1 = get_N(A1, E_vals, bw=bw, I0=I0, truncate=truncate, n=n)
    N2 = get_N(A2, E_vals, bw=bw, I0=I0, truncate=truncate, n=n)

    with np.errstate(divide='ignore'):
        CNR = np.where((N1 != 0) & (N2 != 0), u_c /
                       np.sqrt((1 / N1) + (1 / N2)), 0)

    return CNR


def get_N(A, E_vals, bw=1e-2, I0=1, truncate=4, n=50):

    # Calculates a n-length Gaussian kernel, with points
    # ranging from minus to plus truncate * standard deviation
    # (i.e., for sd=1, truncate=4: ranges from [-4,4]
    G = np.exp(-0.5 * np.linspace(-truncate, truncate, n)**2)
    G /= G.sum()

    # standard deviations in keV, assuming FWHMs of E_vals*bw
    sd = E_vals * bw / (2*np.sqrt(2*np.log(2)))

    # averaging neighborhood radii, in keV
    r = truncate * sd

    # Each row i is a linspace from (E_i-r_i) to (E_i+r_i)
    # Boundaries are handles by padding with E_min and E_max
    Ep = np.array([np.linspace(E-w, E+w, n) for E, w in zip(E_vals, r)])
    Ep[(Ep - E_vals.min()) < 0] = E_vals.min()
    Ep[(Ep - E_vals.max()) > 0] = E_vals.max()

    # Linear interpolation function for A
    # A_int = interp1d(E_vals, A)
    A_int = log_interp(E_vals, A, Ep)

    # Summing over Ep for each E in E_vals
    # N = I0 * (G * np.exp(-A_int(Ep))).sum(axis=-1)
    N = I0 * (G * np.exp(-A_int)).sum(axis=-1)
    return N.round(16)
