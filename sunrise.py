#! /usr/bin/env python3.2
# This is a sunrise and sunset calculator.

import sys
import math
import json

from arguments import Arguments
import orbit
import celestial_coords
import horizon_coords
import utils
import datetime
from rise_set import RiseSet, RiseSetUTCJsonEncoder

J2000_DATE = datetime.date(2000, 01, 01)
JAN_1_2012 = datetime.date(2012, 01, 01)

def main():
    print(sys.argv)

    phi = 42.3583 * math.pi / 180
    lw = 0;

    a = Arguments(sys.argv)

    if a.has_errors():
        a.print_error()
        return

    if a.is_lat_given():
        phi = a.latitude * math.pi / 180

    if a.is_long_given():
        lw = a.longitude * math.pi / 180        

    if a.is_date_given():
        delta_t = a.date_arg - J2000_DATE
        d = delta_t.days - 1
        day_of_year = a.date_arg.timetuple().tm_yday - 1
        t0_utc = utils.t0_utc(d)
        lambda_s = orbit.lambda_s(t0_utc)
        cel_coords = celestial_coords.from_ecliptic_coords(lambda_s)
        delta = cel_coords[0]
        alpha = cel_coords[1]
        t_rise_utc = horizon_coords.t_rise_utc(cel_coords, phi, lw, t0_utc)
        t_set_utc = horizon_coords.t_set_utc(cel_coords, phi, lw, t0_utc)
        print_str = "day: " + str(day_of_year)
        print_str += ", sunrise: " + str(utils.hours(t_rise_utc)) + ":" + str(round(utils.minutes(t_rise_utc) + float(utils.seconds(t_rise_utc))/60, 3))
        print_str += ", sunset: " + str(utils.hours(t_set_utc)) + ":" + str(utils.minutes(t_set_utc)) + ":" + str(utils.seconds(t_set_utc))
        print(print_str) 
        return

    # Calculate rise set times for latitudes ranging from -65 to 65 degrees at 5 degree increments
    rs = [[]]
    for p in range(-13, 14):
        i = 0
        phi = (p * 5) * math.pi / 180
        rs.append([])
        while i < 366:
            delta_t = JAN_1_2012 - J2000_DATE + datetime.timedelta(1)*i
            d = delta_t.days
            t0_utc = utils.t0_utc(d)
            lambda_s = orbit.lambda_s(t0_utc)
            cel_coords = celestial_coords.from_ecliptic_coords(lambda_s)
            delta = cel_coords[0]
            alpha = cel_coords[1]
            t_rise_utc = horizon_coords.t_rise_utc(cel_coords, phi, lw, t0_utc)
            t_set_utc = horizon_coords.t_set_utc(cel_coords, phi, lw, t0_utc)
            date1 = J2000_DATE + delta_t
            
            rs_current = RiseSet(date1, t_rise_utc, t_set_utc)
            rs[p + 13].append(rs_current)
            day_of_year = date1.timetuple().tm_yday - 1
            print_str = str(rs_current.get_day_of_year())
            print_str += ", sunrise: " + str(utils.hours(t_rise_utc)) + ":" + str(round(utils.minutes(t_rise_utc) + float(utils.seconds(t_rise_utc))/60, 3))
            print_str += ", sunset: " + str(utils.hours(t_set_utc)) + ":" + str(round(utils.minutes(t_set_utc) + float(utils.seconds(t_set_utc))/60, 3))
            i = i + 1

    with open("rise_set_data.js", mode="w") as f:
        json.dump(rs, f, indent=2, cls=RiseSetUTCJsonEncoder)

    print("Calculated rise/set times, placed in rise_set_data.js.")

main()

