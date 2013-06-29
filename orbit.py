# Takes care of calculations to do with Earth's motion in its orbit.

import math

S_TROP_DAY = 86400
N_DAY = 0.985600281 * math.pi / 180 # radians per tropical day, ie per 86400 s
N_SEC = N_DAY / S_TROP_DAY # radians per second

T_J2000 = 0

LAMBDA_J2000 = 100.46435 * math.pi / 180
OMEGA_BAR_J2000 = 102.94719 * math.pi / 180

M_J2000 = LAMBDA_J2000 - OMEGA_BAR_J2000 + 2 * math.pi 

def _m_t(t):
    return M_J2000 + N_SEC * (t - T_J2000)

def _c(m):
    C_1 = 1.9148 * math.pi / 180
    C_2 = 0.02 * math.pi / 180
    C_3 = 0.03 * math.pi / 180
   
    return C_1 * math.sin(m) + C_2 * math.sin(2 * m) + C_3 * math.sin(3 * m)

def _nu_s(t):
    m = _m_t(t)
    nu_e = m + _c(m)
    nu_s = nu_e + math.pi
    return nu_s % (2 * math.pi)

def lambda_s(t): # time in seconds since J2000
    return (_nu_s(t) + OMEGA_BAR_J2000) % (2 * math.pi)

