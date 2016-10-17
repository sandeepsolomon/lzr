import time
import os
tzname = ('UTC')
t = os.stat('check.py').st_ctime
t = time.localtime(t)
formatted = time.strftime('%Y-%m-%d %H:%M:%S', t)
print formatted
tz = str.format('{0:+06.2f}', float(time.timezone) / 3600)
print tz
final = formatted + tz
print(final)



from datetime import datetime
import pytz
utc_time = datetime.utcnow()
tz = pytz.timezone('America/St_Johns')

utc_time =utc_time.replace(tzinfo=pytz.UTC) #replace method
st_john_time=utc_time.astimezone(tz)        #astimezone method
print(st_john_time)




