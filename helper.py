from dateutil import parser
import schedule
import datetime

scheduled_jobs = []  # Global list to store scheduled job details

def convert_to_human_readable(timestamp_str):
    # Parse the timestamp
    dt = parser.parse(timestamp_str)
    
    # Format to a more human-readable form
    # Example: "Thursday, November 30, 2023, at 08:30 AM"
    human_readable = dt.strftime("%A, %B %d, %Y, at %I:%M %p")
    return human_readable

#events for day or week
def events_for(events, timeframe):
    today = datetime.date.today()
    if timeframe == "day":
        todays_events = [event for event in events if parser.parse(event['date']).date() == today]
        return todays_events
    else:
        end_of_week = today + datetime.timedelta(days=7)
        weeks_events = [event for event in events if today <= parser.parse(event['date']).date() <= end_of_week]
        return weeks_events

def print_scheduled_jobs():
    print("Scheduled Jobs:")
    for title, datetime_str in scheduled_jobs:
        print(f"Event: {title}, Scheduled at: {datetime_str}")


def print_events_for_today(events):
    today = datetime.date.today()
    todays_events = [event for event in events if parser.parse(event['date']).date() == today]
    print("Events for Today:")
    for event in todays_events:
        date = convert_to_human_readable(event['date'])
        print(f"{event['title']} at {date}")

def print_events_for_week(events):
    today = datetime.date.today()
    end_of_week = today + datetime.timedelta(days=7)
    weeks_events = [event for event in events if today <= parser.parse(event['date']).date() <= end_of_week]
    print("Events for the Week:")
    for event in weeks_events:
        date = convert_to_human_readable(event['date'])
        print(f"{event['title']} at {date}")