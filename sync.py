import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def fetch_and_save_data():
    print("Retreiving data  ... ")
    file_path = 'events_data.json'
    url = os.getenv("URL")
    print(url)
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

def main():
    fetch_and_save_data()

if __name__ == "__main__":
    main()