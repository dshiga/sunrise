# Convenient holder of input args.

import string
import datetime

class Arguments:

    _NO_INPUT = "no_input"

    def __init__(self, argv):
        n = len(argv)

        self.error = "no_error"
        self.error_on_first_arg = False
        self.date_mode = "no_input"
        self.lat_mode = "no_input"
        self.long_mode = "no_input"
 
        if n > 1:
            self._init_date(argv[1])
            if self.has_errors():
                self.error = "no_error"
                self._init_lat(argv[1])
        if n > 2:
            if self.is_date_given():
                self._init_lat(argv[2])
            else:
                self._init_long(argv[2])
        if n > 3:
            if self.is_date_given():
                self._init_long(argv[3])

    def _init_date(self, date_str):
        date_parts = string.split(date_str, "/")
        
        if len(date_parts) != 3:
            self.error = "Date input must be in format mm/dd/yyyy."
        else:
            try:
                month = int(date_parts[0])
                day = int(date_parts[1])
                year = int(date_parts[2])
                self.date_arg = datetime.date(year, month, day)
            except ValueError as e:
                self.error = "Date input must be in format mm/dd/yyyy."
                self.error_on_first_arg = True
        if self.error == "no_error":
            self.date_mode = "date_given"

    def _init_lat(self, lat_str):
        try:
            self.latitude = float(lat_str)
            self.lat_mode = "lat_given"
        except ValueError as e:
            self.error = "Could not parse latitude."
            if self.is_date_given() != True:
                self.error_on_first_arg = True

    def _init_long(self, long_str):
        try:
            self.longitude = float(long_str)
            self.long_mode = "long_given"
        except ValueError as e:
            self.error = "Could not parse longitude."

    def has_errors(self):
        return self.error != "no_error"

    def print_error(self):
        if self.error_on_first_arg:
            print("Arguments must be in format: [mm/dd/yyyy] [latitude [longitude]] (no brackets)")
        else:
            print(self.error)

    def is_date_given(self):
        return self.date_mode != "no_input"

    def is_lat_given(self):
        return self.lat_mode != "no_input"

    def is_long_given(self):
        return self.long_mode != "no_input"
