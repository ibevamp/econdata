from dateutil import parser
from datetime import datetime
from discord import *

import requests
import schedule
import datetime
import time
import pytz
import os
import json


# Path to the local file where JSON data will be saved
json_file_path = 'events_data.json'
scheduled_jobs = []  # Global list to store scheduled job details

def convert_to_human_readable(timestamp_str):
    # Parse the timestamp
    dt = parser.parse(timestamp_str)
    
    # Format to a more human-readable form
    # Example: "Thursday, November 30, 2023, at 08:30 AM"
    human_readable = dt.strftime("%A, %B %d, %Y, at %I:%M %p")
    return human_readable

def fetch_and_save_data(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter for USD events
        usd_events = [event for event in data if event.get('country') == 'USD']
        with open(file_path, 'w') as file:
            json.dump(usd_events, file, indent=4)

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def data_needs_update(file_path):
    # Check if file exists and is updated within the last 24 hours
    if os.path.exists(file_path):
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if (datetime.datetime.now() - last_modified).days < 1:
            return False
    return True

def schedule_news(events):
    for event in events:
        event_time = parser.parse(event['date'])

        #---------------
        # This 5 min parameter will notify users 5 mins before the event.
        # Change it to affect the notification time.
        #---------------
        reminder_time = event_time - datetime.timedelta(minutes=0)


        current_time = datetime.datetime.now(pytz.utc)
        if reminder_time > current_time:
            reminder_time_str = reminder_time.strftime("%H:%M")  # Extract only the time part
            job = schedule.every().day.at(reminder_time_str).do(send_single, event)
            # Store the full date and time for printing
            full_datetime_str = reminder_time.strftime("%Y-%m-%d %H:%M")
            scheduled_jobs.append((event['title'], full_datetime_str))


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

def schedule_daily_tasks(events):
    schedule.every().day.at("16:44").do(send_full, events, "Day")
    schedule.every().day.at("00:01").do(send_full, events, "Week")

def main():
    # url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

    # if data_needs_update(json_file_path):
    # fetch_and_save_data(url, json_file_path)

    events = load_data(json_file_path)
    # send_to_discord(events)
    schedule_daily_tasks(events)
    schedule_news(events)
    
    # # Example usage
    # event = {
    #     "title": "New Home Sales",
    #     "country": "USD",
    #     "date": "2023-11-27T10:00:00-05:00",
    #     "impact": "Medium"
    # }
    
    # send_single(event)

    # Print the scheduled jobs
    # print_scheduled_jobs()
    print_events_for_today(events)
    # print_events_for_week(events)
    # send_full(events, "Week")
    try:
        while True:
            schedule.run_pending()
            print(f"Timestamp: {datetime.datetime.now()}")
            time.sleep(1)  # Adjust the sleep time as needed
    except (KeyboardInterrupt, SystemExit):
        pass
        

if __name__ == "__main__":
    main()
