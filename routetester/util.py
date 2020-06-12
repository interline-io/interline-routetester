import parsedatetime
import pytz
from datetime import datetime

def when(value, tz=None):
    dt = None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str) and value[-1] == "Z":
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        cal = parsedatetime.Calendar()
        dt, _ = cal.parseDT(datetimeString=value, tzinfo=pytz.timezone(tz or 'UTC'))
    return dt

def join(values):
    return ','.join(map(str, values))

def assert_approx_equal(a, b, tolerance=0.0001):
    v = abs(a-b)
    if v > tolerance:
        raise Exception("Not approx equal: expect %s, got %s"%(a, b))
        