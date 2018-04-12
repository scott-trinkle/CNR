from sympy import *

u1, u2, d, s, r, N0, c, m = symbols(
    'u1 u2 d s r N0 c m', positive=True, real=True)

N1 = N0 * exp(-u1 * d)
N2 = N0 * exp(-u1 * d - u2 * r)

V1 = c * pi**2 / m * (1 / N1)
V2 = c * pi**2 / m * (1 / N2)

SNR = simplify(Abs(u1 - u2) / sqrt(V1 + V2))

u_c = u1 + u2
d_c = r

u_m = u1
d_m = d

N_m = N0 * exp(-u_m * d_m)
N_c = N0 * exp(-u_m * d_m - u_c * d_c)

V1 = c * pi**2 / m * (1 / N1)
V2 = c * pi**2 / m * (1 / N2)

SNR = simplify(Abs(u_c - u_m) / sqrt(V1 + V2))
