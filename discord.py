from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv

import os
import datetime
import requests

load_dotenv()
VAMP = os.getenv("VAMP")
#Day suffix ie. Thursday the 5th
def get_day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]


def send_single(event):
    webhook_url = VAMP
    event_time = parser.parse(event['date'])
    formatted_time = event_time.strftime("%A, %B %d, %Y, at %I:%M %p")
    impact_level = f"Impact Level: **{event['impact']}**"

    # Convert color from hex to integer
    if event['impact'] == "High":
        color = 0xff0000  # Red
    elif event['impact'] == "Medium":
        color = 0xff7300  # Orange
    else:
        color = 0x5a965b  # Green

    embed = {
        "title": event['title'],
        "color": color,
        "description": f"{formatted_time} \n{impact_level}",
        "author": {
            "name": "Economic Calendar",
            "url": "https://forexfactory.com"
        }
    }
    
    # Send the embed
    payload = {
        "content": None,
        "embeds": [embed],
        "attachments": []
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code}")
    
def send_full(events, timeframe):
    webhook_url = VAMP

    now = datetime.datetime.now()
    day = now.day
    month = now.strftime("%B")
    year = now.year
    suffix = get_day_suffix(day)

    date_with_suffix = f"{month} the {day}{suffix} of {year}"

    if timeframe == "Day":            
        title = f"Events for {date_with_suffix}"
    else:
        title = f"Events for Week of {date_with_suffix}"
    
    # Create the embed structure
    embed = {
        "title": title,
        "color": 5814783,
        "fields": [],
        "author": {
            "name": "Economic Calendar",
            "url": "https://forexfactory.com",
        }
    }

    # Add each event to the fields of the embed
    for event in events:
        event_time = parser.parse(event['date'])
        formatted_time = event_time.strftime("%A, %B %d, %Y, at %I:%M %p")
        impact_level = f"Impact Level: **{event['impact']}**"
        embed['fields'].append({
            "name": event['title'],
            "value": f"{formatted_time} \n{impact_level}"
        })

    # Send the embed
    payload = {
        "content": None,
        "embeds": [embed],
        "attachments": []
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code}")
