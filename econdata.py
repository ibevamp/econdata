from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv
from discord import *
from helper import *
from apscheduler.schedulers.background import BackgroundScheduler

import requests
import schedule
import datetime
import time
import pytz
import os
import json

load_dotenv()
url = os.getenv("url")

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Path to the local file where JSON data will be saved
json_file_path = 'econdata/events_data.json'


# Function to print all scheduled jobs
def print_scheduled_jobs():
    jobs = scheduler.get_jobs()
    print("Scheduled Jobs:")
    for job in jobs:
        print(f"Job ID: {job.id}, Next Run: {job.next_run_time}, Job Function: {job.func.__name__}")


def clear_schedule():
    schedule.clear()
    print("All scheduled tasks have been cleared.")

def fetch_and_save_data():
    print("Retreiving data  ... ")
    file_path = 'events_data.json'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter for USD events
        usd_events = [event for event in data if event.get('country') == 'USD']
        with open(file_path, 'w') as file:
            json.dump(usd_events, file, indent=4)
        print("Updated Events JSON")
        
    else:
        print("Error retreiving data")

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def schedule_news(events):
    for event in events:
        event_time = parser.parse(event['date'])
        reminder_time = event_time - datetime.timedelta(minutes=0)  # 5 minutes before the event

        # Schedule each event
        scheduler.add_job(send_single, 'date', run_date=reminder_time, args=[event])

def schedule_daily_tasks(events):
    # Schedule daily tasks
    scheduler.add_job(send_full, 'cron', day_of_week='mon-sun', hour=6, minute=00, second=0, args=[events, "Day"])

def schedule_weekly_tasks(events):
    # Schedule weekly task
    scheduler.add_job(fetch_and_save_data, 'cron', day_of_week='sun', hour=19, minute=00, second=0)

def main():
    json_file_path = 'events_data.json'
    events = load_data(json_file_path)

    schedule_weekly_tasks(events)
    schedule_daily_tasks(events)
    schedule_news(events)
    
    print_events_for_today(events)
    print_scheduled_jobs()
    try:
        # Keep the script running
        while True:
            schedule.run_pending()
            print(f"Timestamp: {datetime.datetime.now()}")
            time.sleep(30)  # Adjust the sleep time as needed
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)

if __name__ == "__main__":
    main()
        # send_to_discord(events)
        # Print the scheduled jobs
        #print_scheduled_jobs()
        #print_events_for_today(events)
        # print_events_for_week(events)
        # # Example usage
        # event = {
        #     "title": "New Home Sales",
        #     "country": "USD",
        #     "date": "2023-11-27T10:00:00-05:00",
        #     "impact": "Medium"
        # }
        
        # send_single(event)
        # send_full(events, "Week")