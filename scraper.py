import requests
import json
import os
import argparse

# Constants
DATA_FILE = "data/rentals.json"
TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage"

def get_api_response(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.yad2.co.il/",
        "Origin": "https://www.yad2.co.il",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        text = response.text
        if not text or not text.strip():
            print(f"Error: Empty response from API (status {response.status_code})")
            return None
        return response.json()
    except (json.JSONDecodeError, requests.exceptions.JSONDecodeError) as e:
        snippet = (response.text[:200] + "..." if len(response.text) > 200 else response.text) if response.text else "(empty)"
        print(f"Error decoding JSON: {e}")
        print(f"Response status: {response.status_code}, body snippet: {snippet!r}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_items(data):
    if not data or 'data' not in data or 'markers' not in data['data']:
        return []
    
    items = []
    for marker in data['data']['markers']:
        token = marker.get('token')
        if not token:
            continue
            
        # Extract details for the message
        street = marker.get('address', {}).get('street', {}).get('text', 'Unknown Street')
        city = marker.get('address', {}).get('city', {}).get('text', 'Unknown City')
        price = marker.get('price', 'N/A')
        rooms = marker.get('additionalDetails', {}).get('roomsCount', 'N/A')
        
        item_url = f"https://www.yad2.co.il/item/{token}"
        
        items.append({
            'id': token,
            'url': item_url,
            'details': f"{street}, {city} - {rooms} rooms - {price} NIS"
        })
    
    return items

def load_saved_data():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def notify_telegram(message):
    token = os.environ.get("API_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not token or not chat_id:
        print("Telegram credentials not found. Skipping notification.")
        print(f"Message would have been:\n{message}")
        return

    url = TELEGRAM_API_URL.format(token)
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending Telegram notification: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Yad2 Rental Scraper")
    parser.add_argument(
        "--api-url",
        required=True,
        help="Yad2 API URL with search parameters (e.g. https://gw.yad2.co.il/realestate-feed/rent/map?city=...)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clear the rentals DB before running (treat all listings as new)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    api_url = (args.api_url or "").strip()

    if not api_url or not api_url.startswith("http"):
        print("Error: API URL is required and must start with http")
        return

    if args.clean:
        save_data([])
        print("Rentals DB cleared.")

    print(f"Starting API scrape for: {api_url}")
    data = get_api_response(api_url)

    if not data:
        print("Failed to retrieve data.")
        return

    current_items = extract_items(data)
    saved_ids = load_saved_data()

    new_items = []
    current_ids = []

    for item in current_items:
        current_ids.append(item['id'])
        if item['id'] not in saved_ids:
            new_items.append(item)

    if new_items:
        print(f"Found {len(new_items)} new items.")

        # Prepare message
        messages = []
        messages.append(f"Found {len(new_items)} new listing(s):")
        for item in new_items:
            messages.append(f"{item['details']}\n{item['url']}")

        full_message = "\n\n".join(messages)
        notify_telegram(full_message)

        # Append new IDs to history to avoid re-notifying.
        # Keeping history is safer than syncing with current state,
        # in case an item temporarily disappears from the API.
        updated_saved_ids = list(set(saved_ids + current_ids))
        save_data(updated_saved_ids)

        # Create a flag file to trigger git push
        with open("push_me", "w") as f:
            f.write("")
    else:
        print("No new items found.")


if __name__ == "__main__":
    main()
