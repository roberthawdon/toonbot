from datetime import datetime
from threading import Timer

def runat(target, tolerance):
    runat = datetime.strptime(target, "%H:%M:%S")
    x=datetime.utcnow()
    y=x.replace(day=x.day, hour=runat.hour, minute=runat.minute, second=runat.second, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1

    tbefore = tolerance/2
    tafter = 86400 - tolerance/2

    if secs < tbefore or secs > tafter:
        return True
    else:
        return False

def workhourscheck(starttime, endtime, tzoffset):
    currenttime = datetime.utcnow()
    midnight = datetime.strptime("00:00:00", "%H:%M:%S")
    lowertime = datetime.strptime(starttime, "%H:%M:%S")
    uppertime = datetime.strptime(endtime, "%H:%M:%S")
    lower = (lowertime-midnight).seconds-tzoffset
    if lower < 0:
        lower = lower+86400
    upper = (uppertime-midnight).seconds-tzoffset
    if upper > 86400:
        upper = upper-86400
    current = (currenttime-midnight).seconds

    if lower < upper:
        if current > lower and current < upper:
            return True
        else:
            return False
    else:
        if current > lower or current < upper:
            return True
        else:
            return False
