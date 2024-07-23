import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
BASE_URL = "https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations/"
NUM_REQUESTS = 100000
MAX_RETRIES = 3
RETRY_DELAY = 0.1  # Delay between retries
RATE_LIMIT = 1 / 344  # Targeting 344 requests per second

def fetch_user_data(user_id):
    """Fetch user data from the API."""
    url = f"{BASE_URL}{user_id}"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, timeout=10)  # Set a timeout for each request
            response.raise_for_status()
            data = response.json()

            user_data = {
                "user_id": int(data["data"]["user_id"]["N"]),
                "latitude": float(data["data"]["latitude"]["N"]),
                "longitude": float(data["data"]["longitude"]["N"]),
            }
            print(f"Fetched data for user ID {user_id}")
            return user_data

        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Error fetching data for user ID {user_id}: {e} (Retry {retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

    print(f"Failed to fetch data for user ID {user_id} after {MAX_RETRIES} retries")
    return None

def main():
    results = []
    with ThreadPoolExecutor(max_workers=344) as executor:
        start_time = time.time()

        for user_id_batch in range(0, NUM_REQUESTS, 344):
            # Submit a batch of 344 requests
            futures = {executor.submit(fetch_user_data, user_id): user_id for user_id in range(user_id_batch, min(user_id_batch + 344, NUM_REQUESTS))}

            for future in as_completed(futures):
                user_id = futures[future]
                try:
                    user_data = future.result()
                    if user_data:
                        results.append(user_data)
                except Exception as exc:
                    print(f"Unhandled error processing user ID {user_id}: {exc}")

            # Rate limit handling
            elapsed_time = time.time() - start_time
            expected_time = (user_id_batch + 344) * RATE_LIMIT
            if elapsed_time < expected_time:
                time.sleep(expected_time - elapsed_time)

    # Save all results to CSV at the end
    with open("/assets/user_locations.csv", "w", newline="") as csvfile:
        fieldnames = ["user_id", "latitude", "longitude"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row

        for user_data in results:
            writer.writerow(user_data)

    print("User data has been saved to user_locations.csv")

if __name__ == "__main__":
    main()
