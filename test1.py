import random
import time

import requests

from backend.web.dao.artwalk.places_dao import PlacesDAO
from backend.web.dao.artwalk.routes_dao import RoutesDAO

# Replace with your Google Maps API key
API_KEY = "AIzaSyBHNVBV2-gb5Jl-b84JeGt6zsMWLZ6E8J8"


def get_walking_distances(origins, destinations):
    """
    This function retrieves walking distances between origin and destination pairs
    using the Distance Matrix API and inserts them into the walking_distances table.

    Args:
        origins (list): List of origin locations (dictionaries with latitude/longitude).
        destinations (list): List of destination locations (dictionaries with latitude/longitude).
    """
    if not API_KEY:
        print("Error: Google Maps API key is not set.")
        return

    if not origins or not destinations:
        print("Error: Origin and destination lists must not be empty.")
        return

    # Base URL for Distance Matrix API requests
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

    # Set walking as travel mode
    travel_mode = "walking"

    # Extract latitude and longitude from origin/destination dictionaries
    origin_lat_lngs = [f"{origin['latitude']},{origin['longitude']}" for origin in origins]
    destination_lat_lngs = [f"{dest['latitude']},{dest['longitude']}" for dest in destinations]

    # Construct request parameters
    params = {
        "origins": "|".join(origin_lat_lngs),
        "destinations": "|".join(destination_lat_lngs),
        "mode": travel_mode,
        "key": API_KEY
    }

    try:
        # Send request and get response
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad requests
    except requests.RequestException as e:
        print(f"Error during API request: {e}")
        return

    # Parse JSON response
    data = response.json()

    # Extract walking distances
    for origin_index, origin_data in enumerate(data.get("rows", [])):
        for destination_index, destination_data in enumerate(origin_data.get("elements", [])):
            distance = destination_data.get("distance", {}).get("value")
            duration = destination_data.get("duration", {}).get("value")  # Assuming duration in seconds

            if distance is not None and duration is not None:
                # Get origin and destination IDs using their locations
                origin_location = origins[origin_index]
                destination_location = destinations[destination_index]
                origin_id = places_dao.get_place_id_by_location(origin_location)
                destination_id = places_dao.get_place_id_by_location(destination_location)

                if origin_id and destination_id:
                    # Insert walking distance using RoutesDAO
                    routes_dao.insert_route(origin_id, destination_id, distance, duration, None)
                else:
                    print(
                        f"Place ID not found for origin or destination. Skipping insertion for origin: {origin_location} and destination: {destination_location}")
            else:
                print(
                    f"Missing distance or duration data for origin: {origins[origin_index]} and destination: {destinations[destination_index]}")


# Example usage
places_dao = PlacesDAO()
routes_dao = RoutesDAO()
origins = places_dao.read_all_locations()
dests = places_dao.read_all_locations()

# Reverse the lists to traverse from end to start
origins.reverse()
dests.reverse()


# Chunking the list into smaller lists of 10 elements each
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


# Process chunks of 10 origins and destinations at a time
origin_chunks = list(chunk_list(origins, 10))
dest_chunks = list(chunk_list(dests, 10))

total_origin_chunks = len(origin_chunks)
total_dest_chunks = len(dest_chunks)

for i, origin_chunk in enumerate(origin_chunks):
    for j, dest_chunk in enumerate(dest_chunks):
        get_walking_distances(origin_chunk, dest_chunk)
        remaining_origin_chunks = total_origin_chunks - i - 1
        remaining_dest_chunks = total_dest_chunks - j - 1
        print(
            f"Remaining origin chunks: {remaining_origin_chunks}, Remaining destination chunks: {remaining_dest_chunks}")
        # Wait between 30 seconds to 1 minute
        wait_time = random.randint(10, 30)
        print(f"Waiting for {wait_time} seconds before next API call.")
        time.sleep(wait_time)
