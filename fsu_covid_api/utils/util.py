import time
from typing import Union
from datetime import date, datetime

def time_to_epoch(input: Union[int, float, date, datetime]):
    if isinstance(input, datetime) or isinstance(input, date):
        return int(time.mktime(input.timetuple())-18000)
    elif isinstance(input, int) or isinstance(input, float):
        return int(input)-18000 # EST to GMT