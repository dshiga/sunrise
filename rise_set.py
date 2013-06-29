import json

class RiseSet:
    def __init__(self, date, rise_time, set_time):
        self.date = date
        self.rise_time = rise_time
        self.set_time = set_time

    def get_day_of_year(self):
        """Returns day of year as integer, where 0 is Jan 1 and Dec 31 is 365, 
        or 366 if the date falls in a leap year.""" 
        return self.date.timetuple().tm_yday - 1

    def get_rise(self):
        """Returns a float between 0 and 24 representing rise time in hours since midnight utc."""
        return 24 * self.rise_time / 86400;

    def get_set(self):
        """Returns a float between 0 and 24 representing set time in hours since midnight utc."""
        return 24 * self.set_time / 86400;
    
    def get_rise_est(self):
        """Returns the rise time in hours since midnight EST"""
        result = self.get_rise() - 5.0;
        if result < 0:
            result += 24;
        return result;

    def get_set_est(self):
        """Returns the set time in hours since midnight EST"""
        result = self.get_set() - 5.0;
        if result < 0:
            result += 24;
        return result;

class RiseSetUTCJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, RiseSet):
            return "object"
        
        return {
                "day": obj.get_day_of_year(),
                "rise": obj.get_rise(),
                "set": obj.get_set()
               }

class RiseSetESTJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, RiseSet):
            return "object"
        
        return {
                "day": obj.get_day_of_year(),
                "rise": obj.get_rise_est(),
                "set": obj.get_set_est()
               }

