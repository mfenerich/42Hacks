import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor

# Constants
EARTH_RADIUS_KM = 6371.0

# Haversine formula to calculate the distance between two points (vectorized)
def haversine_vectorized(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return EARTH_RADIUS_KM * c

# Function to find the closest airport by calculating distance using vectorized Haversine
def find_closest_airport(user_lat, user_lon, airports_df):
    airport_lats = airports_df['latitude_deg'].values
    airport_lons = airports_df['longitude_deg'].values
    
    distances = haversine_vectorized(user_lat, user_lon, airport_lats, airport_lons)
    
    min_index = np.argmin(distances)
    closest_airport = airports_df.iloc[min_index]
    
    return closest_airport

# Function to process a chunk of user data
def process_chunk(chunk, airports_df):
    results = []
    
    user_lats = chunk['latitude'].values
    user_lons = chunk['longitude'].values
    
    # Process each user
    for user_id, user_lat, user_lon in zip(chunk['user_id'], user_lats, user_lons):
        # Print the user being processed
        print(f"Processing user ID: {user_id}")
        
        closest_airport = find_closest_airport(user_lat, user_lon, airports_df)
        
        if closest_airport is not None:
            results.append({
                'user_id': user_id,
                'closest_airport_id': closest_airport['id']
            })
    
    return results

# Function to process data in parallel
def parallel_processing(user_locations, airports_df, chunk_size=10000):
    results = []
    
    # Create chunks
    chunks = [user_locations[i:i + chunk_size] for i in range(0, len(user_locations), chunk_size)]
    
    # Process chunks in parallel
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk, airports_df) for chunk in chunks]
        for future in futures:
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Error processing chunk: {e}")
    
    return results

if __name__ == '__main__':
    # Load the CSV files
    user_locations = pd.read_csv('/assets/user_locations.csv')
    airports = pd.read_csv('/assets/airports_w_wiki.csv')

    # Perform parallel processing
    chunk_size = 10000
    all_results = parallel_processing(user_locations, airports, chunk_size)

    # Convert results to DataFrame
    results_df = pd.DataFrame(all_results)

    # Save the results to a new CSV file
    results_df.to_csv('/assets/user_closest_airports.csv', index=False)

    print("Closest airports for each user have been calculated and saved to 'user_closest_airports.csv'.")
