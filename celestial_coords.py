import math

EPSILON = 23.45 * math.pi / 180

def from_ecliptic_coords(lambda_s):
    delta = math.asin(math.sin(lambda_s) * math.sin(EPSILON))
    alpha = math.atan2(math.tan(lambda_s), math.cos(EPSILON))
    if alpha < 0:
        if math.sin(lambda_s) < 0:
            alpha = alpha + math.pi * 2
        else:
            alpha = alpha + math.pi
    if alpha > 0 and alpha < math.pi / 2:
        if math.cos(lambda_s) < 0:
            alpha = alpha + math.pi
    return delta, alpha

