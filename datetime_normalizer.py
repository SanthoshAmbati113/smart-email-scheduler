from datetime import datetime, time

DEFAULT_TIME = time(10, 0)

def normalize_event(event):
    if event.time is None or event.time == "null":
        event_time = DEFAULT_TIME
    else:
        event_time = datetime.strptime(event.time, "%H:%M").time()

    dt = datetime.combine(event.date, event_time)
    return dt
