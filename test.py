import ast
import time

from backend.web.dao.artwalk.places_dao import PlacesDAO
from backend.web.dao.artwalk.routes_dao import RoutesDAO
from backend.web.service.artwalk.google_maps import GoogleMaps


def main():
    travel_mode = "WALK"
    api_key = "AIzaSyCGygp0SRJldfPq7nWt7kPNtaJ168VZH7E"  # Replace with your actual Google Maps API key
    google_maps = GoogleMaps(api_key)

    RoutesDAO().create_table()
    origins = PlacesDAO().read_all_locations()
    dests = PlacesDAO().read_all_locations()

    starting_origin = PlacesDAO().read_place("ChIJ_RZ56lFgLxMRklRuHfxWXP8")
    starting_dest = PlacesDAO().read_place("ChIJDXtMH2FgLxMRrs22RFSAHKI")

    origin_loc = ast.literal_eval(starting_origin[3])
    dest_loc = ast.literal_eval(starting_dest[3])

    origin_start_index = origins.index(origin_loc) - 1
    dest_start_index = origins.index(dest_loc) - 1

    for origin_index in range(origin_start_index, len(origins)):
        for dest_index in range(dest_start_index, len(dests)):
            print(f"Processing route {origin_index + 1}/{len(origins)} - {dest_index + 1}/{len(dests)}")
            distance, duration, polyline = google_maps.get_distance_time(
                origins[origin_index]['latitude'], origins[origin_index]['longitude'],
                dests[dest_index]['latitude'], dests[dest_index]['longitude'],
                travel_mode
            )
            RoutesDAO().insert_route(
                PlacesDAO().read_id_by_location(str(origins[origin_index])),
                PlacesDAO().read_id_by_location(str(dests[dest_index])),
                distance, duration, polyline
            )
            time.sleep(1)
        # Reset destination index to 0 after the first run of the inner loop
        dest_start_index = 0


if __name__ == "__main__":
    main()
