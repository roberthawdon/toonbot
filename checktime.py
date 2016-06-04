from datetime import datetime
from threading import Timer

def runat(target, tolerance):
    runat = datetime.strptime(target, "%H:%M:%S" )
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
