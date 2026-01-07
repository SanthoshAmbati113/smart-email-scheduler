from calendar_utils import to_rfc3339

def create_calendar_event(service, title, start_dt, end_dt=None):
    if end_dt is None:
        end_dt = start_dt

    event_body = {
        "summary": title,
        "start": {
            "dateTime": to_rfc3339(start_dt),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": to_rfc3339(end_dt),
            "timeZone": "Asia/Kolkata",
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    print("✅ Event created:", event.get("htmlLink"))
