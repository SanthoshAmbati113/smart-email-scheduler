from datetime_normalizer import normalize_event
from calendar_service import build_calendar_service
from calendar_events import create_calendar_event
from llm import classify_urgency,extract_events_from_email

# result = YOUR LLM OUTPUT
# result.task_name
# result.events

email_text="""Dear Students, 

Please note that Mess registration is mandatory for every student and students will have access to mess only using face recognition.

You have to submit the below Google form on or before in 15 days

Regards, 
A.Suneetha 
Assistant Manager
Academic Office 
Indian Institute of Information Technology Sri City"""

urgency = classify_urgency(email_text)
print("Urgency:", urgency)

result = extract_events_from_email(email_text)
print(result)


service = build_calendar_service()

start_event = None
end_event = None

# Separate start and end if present
for event in result.events:
    if event.role == "start":
        start_event = normalize_event(event)
    elif event.role == "end":
        end_event = normalize_event(event)
    else:
        dt = normalize_event(event)
        create_calendar_event(
            service,
            result.task_name,
            dt
        )

# If deadline-style start & end
if start_event and end_event:
    create_calendar_event(
        service,
        result.task_name,
        start_event,
        end_event
    )
