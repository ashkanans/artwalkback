import requests

from backend.web.dao.artwalk.places_dao import PlacesDAO


class GoogleMaps:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_text(self, text_query, page_size, nextPageToken=None):
        url = "https://places.googleapis.com/v1/places:searchText"

        # Request headers
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "*"
        }

        # Request body
        data = {
            "textQuery": text_query,
            "pageSize": page_size
        }
        if nextPageToken:
            data["pageToken"] = nextPageToken

        try:
            # Send POST request
            response = requests.post(url, headers=headers, json=data)

            # Check if request was successful
            if response.status_code == 200:
                response_data = response.json()
                if "places" in response_data:
                    PlacesDAO().create_place(response_data['places'])
                else:
                    print("There is no list of places")
                    return

                print("Success:", response.status_code)
                if "nextPageToken" in response_data:
                    self.search_text(text_query, page_size, response_data['nextPageToken'])
                else:
                    print("There is no next page")
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print("Error:", e)

    def get_distance_time(self, origin_lat, origin_lng, dest_lat, dest_lng, travel_mode="WALK"):
        url = "https://maps.googleapis.com/maps/api/directions/json"

        # Request parameters
        params = {
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{dest_lat},{dest_lng}",
            "mode": travel_mode.lower(),
            "key": self.api_key
        }

        try:
            # Send GET request
            response = requests.get(url, params=params)

            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                if "routes" in result and len(result["routes"]) > 0:
                    route = result["routes"][0]["legs"][0]
                    distance = route["distance"]["value"]  # Distance in meters
                    duration = route["duration"]["value"]  # Duration in seconds
                    polyline = result["routes"][0]["overview_polyline"]["points"]
                    return distance, duration, polyline
                else:
                    print("No routes found.")
                    return None, None, None
            else:
                print("Error:", response.status_code, response.text)
                return None, None, None
        except Exception as e:
            print("Error:", e)
            return None, None, None
