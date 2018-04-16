import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


def match_energies(mat1, mat2):
    '''
    Match sampled energy values between two materials along the most densely
    sampled energy array

    Parameters
    __________
    mat1 : cnrgui.material.Material object
        First material
    mat2 : cnrgui.material.Material object
        Second material
    '''

    # Determine which material is more densely sampled
    big, small = (mat1, mat2) if mat1.E_raw.size > mat2.E_raw.size else (
        mat2, mat1)

    # Big energy/u_p does not change
    big.E = big.E_raw
    big.u_p = big.u_p_raw

    # Small is interpolated onto big
    small.E = big.E
    small.u_p = log_interp(small.E_raw, small.u_p_raw, big.E)


def log_interp(x, y, x_new):
    '''
    Calculates a log-log linear interpolation and extrapolation
    along new values.

    Parameters
    __________
    x : ndarray
        Model input
    y : ndarray
        Model output
    x_new : ndarray
        New model input

    Returns
    _______
    new_y : ndarray
        Values interpolated from (x,y) along x_new. Performs extrapolation
        if values of x_new are out of the range of x
    '''

    logx = np.log(x)
    logy = np.log(y)

    # Allows for extrapolation, as opposed to scipy.interpolate.interp1d
    interp_func = InterpolatedUnivariateSpline(logx, logy, k=1)

    new_y = np.exp(interp_func(np.log(x_new)))
    return new_y


def cnr(bg, contrast, I0=1, bw=1e-2, conv=0.1, truncate=4, n=50):
    '''
    Calculates CNR for two-material model.

    Parameters
    __________
    bg : Material
        Background material object with given thickness, density
    contrast: Material
        Contrast material object with given thickness, density
    I0 : int
        Entrance intensity (number of photons)
    bw : float
        Fractional FWHM for intensity spectrum (BW = dE / E)
    conv : float
        Conversion factor from material thickness units to cm
    truncate : int or float
        Number of standard deviations to include for BW averaging
    n : int
        Number of sampling points to use when calculating the Gaussian weights
        for BW averaging


    Returns
    _______
    CNR : ndarray
        Values of CNR at the energy values given by the E attribute of both
        bg and contrast


    Notes
    _____
    (1) bg and contrast should already have matched E vectors using the
        cnrgui.util.match_energies function
    (2) Assumes the following parameter units:

                         I         :  number of photons
                         u_p       :  cm2/g
                         density   :  g / cm3
                         thickness :  mm (default. Specify with 'conv')

    '''

    E_vals = bg.E

    # Mass attenuation to linear attenuation coefficient
    u_c = contrast.u_p * contrast.density
    u_bg = bg.u_p * bg.density

    # Thickness units to cm
    d_c = contrast.thickness * conv
    d_bg = bg.thickness * conv

    # Attenuation projections
    A1 = u_bg * d_bg
    A2 = u_bg * d_bg + u_c * d_c

    # Number of photons
    N1 = get_N(A1, E_vals, bw=bw, I0=I0, truncate=truncate, n=n)
    N2 = get_N(A2, E_vals, bw=bw, I0=I0, truncate=truncate, n=n)

    # Some N values will be 0. The call to np.where sets CNR=0 at
    # those points, but will still throw a NumPy "divide by 0" warning,
    # so I temporarily suspend that warnings.
    with np.errstate(divide='ignore'):
        CNR = np.where((N1 != 0) | (N2 != 0), u_c /
                       np.sqrt((1 / N1) + (1 / N2)), 0)

    return CNR


def get_N(A, E_vals, bw=1e-2, I0=1, truncate=4, n=50):
    '''
    Calculate N, the number of photons through the central point of a
    CNR phantom.

    Parameters
    __________
    A : ndarray
        Attenuation projections as a function of energy
    E_vals : ndarray
        Sampled energy values for A
    bw : float
        Fractional FWHM for intensity spectrum (BW = dE / E)
    I0 : int
        Entrance intensity (number of photons)
    truncate : int or float
        Number of standard deviations to include for BW averaging
    n : int
        Number of sampling points to use when calculating the Gaussian weights
        for BW averaging

    Returns
    _______
    N : ndarray
        Energy-dependent number of photons through center of CNR phantom.

    '''

    # Calculates a n-length Gaussian kernel, with points
    # ranging from minus to plus (truncate * standard deviation)
    # (i.e., for sd=1, truncate=4: ranges from [-4,4]
    G = np.exp(-0.5 * np.linspace(-truncate, truncate, n)**2)
    G /= G.sum()

    # Gaussian standard deviations in keV, assuming FWHMs of E_vals*bw
    sd = E_vals * bw / (2*np.sqrt(2*np.log(2)))

    # averaging neighborhood radii, in keV
    r = truncate * sd

    # Each row i is a linspace from (E_i-r_i) to (E_i+r_i)
    Ep = np.array([np.linspace(E-w, E+w, n) for E, w in zip(E_vals, r)])

    # Boundaries are handles by padding with E_min and E_max
    Ep[(Ep - E_vals.min()) < 0] = E_vals.min()
    Ep[(Ep - E_vals.max()) > 0] = E_vals.max()

    # Interpolated values for A along Ep
    A_int = log_interp(E_vals, A, Ep)

    # Summing over Ep for each E in E_vals
    N = I0 * (G * np.exp(-A_int)).sum(axis=-1)

    return N.round(16)
