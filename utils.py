import math
import orbit

HOUR_SECS = 3600
MIN_SECS = 60
HOUR_MINS = 60

def mod_2_pi(x):
    return x % (2*math.pi)

def hours(t_sec):
    return int(math.floor(t_sec / HOUR_SECS))

def minutes(t_sec):
    return int(math.floor((t_sec - hours(t_sec)*HOUR_SECS)/MIN_SECS))

def seconds(t_sec):
    return int(round(t_sec % MIN_SECS))

def t0_utc(d):
    return (d - 0.5)*orbit.S_TROP_DAY
