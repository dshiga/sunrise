import math
import utils

THETA_J2000 = 280.46 * math.pi / 180
PHI = 42.3583 * math.pi / 180
UTC_DAY_S = 86400
SID_DAY_S = 0.9972695663 * UTC_DAY_S # in seconds
OMEGA = 2 * math.pi / SID_DAY_S

def _gmst(t):
    return THETA_J2000 + OMEGA * (t - J2000) / SID_DAY_S

def _gha(alpha, t):
    return _gmst(t) - alpha

def _ghan(alpha):
    return THETA_J2000 - alpha

def _lha(alpha, lw, t):
    return _gha(t, alpha) - lw

def _lhan(alpha, lw):
    return _ghan(alpha) - lw 

def altitude(cel_coords, phi, lw, t):
    delta = cel_coords[0]
    alpha = cel_coords[1]
    lha = _lha(alpha, lw, t) 
    result = math.asin(math.sin(delta) * math.sin(phi) + math.cos(delta) * math.cos(lha) * math.cos(phi))
    return utils.mod_2_pi(result)

def azimuth(cel_coords, phi, lw, t):
    delta = cel_coords[0]
    alpha = cel_coords[1]
    lha = _lha(alpha, lw, t)
    result = math.atan(math.sin(lha), math.cos(lha) * math.sin(phi) - math.tan(delta) * math.cos(phi))
    return utils.mod_2_pi(result)

def x(delta):
    return math.acos((-math.tan(delta)) * math.tan(PHI))

def t_set_gsid(cel_coords, phi):
    """Returns set time in seconds since last time gmst was theta0"""
    delta = cel_coords[0]
    alpha = cel_coords[1]
    result = (math.acos((-math.tan(delta)) * math.tan(phi)) - _ghan(alpha)) / OMEGA
    if result < 0:
        result += SID_DAY_S
    return result 

def t_rise_gsid(cel_coords, phi):
    """Returns rise time in seconds since last time gmst was theta0"""
    delta = cel_coords[0]
    alpha = cel_coords[1]
    result = (-math.acos((-math.tan(delta)) * math.tan(phi)) - _ghan(alpha)) / OMEGA
    if result < 0:
        result += SID_DAY_S
    return result 

def t_set_utc(cel_coords, phi, lw, t0_utc):
    """Returns time at which object sets, in seconds since midnight utc."""
    result = t_set_gsid(cel_coords, phi) - delta_gmst_theta_0(t0_utc)
    if result < 0:
        result = result + SID_DAY_S
    result += lw / OMEGA
    if result > UTC_DAY_S:
        result = result - UTC_DAY_S
    return result

def t_rise_utc(cel_coords, phi, lw, t0_utc):
    """Returns time at which object rises, in seconds since midnight utc."""
    result = t_rise_gsid(cel_coords, phi) - delta_gmst_theta_0(t0_utc)
    if result < 0:
        result = result + SID_DAY_S
    result += lw / OMEGA
    if result > UTC_DAY_S:
        result = result - UTC_DAY_S
    return result

def delta_gmst_theta_0(t0_utc): # seconds since last time GMST was theta0
    return t0_utc % SID_DAY_S 
