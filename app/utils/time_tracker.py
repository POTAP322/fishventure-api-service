from datetime import datetime
import pytz

moscow_tz = pytz.timezone('Europe/Moscow')

def get_moscow_time():
    return datetime.now(moscow_tz)