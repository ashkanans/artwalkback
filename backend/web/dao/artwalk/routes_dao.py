import datetime
import sqlite3

from backend.database_config.database_artwalk.config import DB_PATH


class RoutesDAO:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create routes table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS routes (
                            originId TEXT,
                            destId TEXT,
                            distanceMeters INTEGER,
                            duration TEXT,
                            encodedPolyline TEXT,
                            created_at TEXT
                        )''')

        conn.commit()
        conn.close()
        print("OK")

    def insert_route(self, originId, destId, distance_meters, duration, encoded_polyline):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if the row with the given originId and destId exists
        cursor.execute('''SELECT distanceMeters, duration FROM routes WHERE originId = ? AND destId = ?''',
                       (originId, destId,))
        existing_row = cursor.fetchone()

        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if existing_row is None:
            # Insert new route data into routes table
            cursor.execute('''INSERT INTO routes (originId, destId, distanceMeters, duration, encodedPolyline, created_at)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (originId, destId, distance_meters, duration, encoded_polyline, created_at))
            print(f"Row with originId: {originId} and destId: {destId} inserted.")
        else:
            distance, duration_val = existing_row
            if distance is not None and duration_val is not None:
                # Skip insertion if distance and duration already exist
                print(
                    f"Row with originId: {originId} and destId: {destId} already exists with distance and duration, skipping insertion.")
            else:
                # Update the existing row with new distance and duration if they are missing
                cursor.execute('''UPDATE routes
                                  SET distanceMeters = ?, duration = ?, encodedPolyline = ?, created_at = ?
                                  WHERE originId = ? AND destId = ?''',
                               (distance_meters, duration, encoded_polyline, created_at, originId, destId))
                print(f"Row with originId: {originId} and destId: {destId} updated.")

        conn.commit()
        conn.close()

    def read_all_routes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch all routes from routes table
        cursor.execute('''SELECT * FROM routes''')
        routes = cursor.fetchall()

        conn.close()
        return routes

    # -----------------------------------------------------------
    def insert_walking_distance(self, origin_id, destination_id, distance_meters, duration):
        """
        Inserts a new walking distance record into the table.

        Args:
            origin_id (str): ID of the origin location.
            destination_id (str): ID of the destination location.
            distance_meters (int): Walking distance in meters.
            duration (int): Walking duration in seconds.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if a record already exists for this origin-destination pair
        cursor.execute('''SELECT * FROM walking_distances WHERE origin_id = ? AND destination_id = ?''',
                       (origin_id, destination_id,))
        existing_row = cursor.fetchone()

        if existing_row is None:
            # Insert new record
            cursor.execute('''INSERT INTO walking_distances (origin_id, destination_id, distance, duration)
                          VALUES (?, ?, ?, ?)''', (origin_id, destination_id, distance_meters, duration))
            print(f"Walking distance from {origin_id} to {destination_id} inserted.")
        else:
            print(f"Walking distance from {origin_id} to {destination_id} already exists, skipping insertion.")

        conn.commit()
        conn.close()

    def read_all_walking_distances(self):
        """
        Fetches all walking distance records from the table.

        Returns:
            list: List of dictionaries, each representing a walking distance record.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch all walking distances
        cursor.execute('''SELECT * FROM walking_distances''')
        distances = cursor.fetchall()

        conn.close()
        return distances

    def get_walking_distance(self, origin_id, destination_id):
        """
        Gets the walking distance for a specific origin-destination pair.

        Args:
            origin_id (str): ID of the origin location.
            destination_id (str): ID of the destination location.

        Returns:
            int: Walking distance in meters, or None if not found.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch walking distance for the specific pair
        cursor.execute('''SELECT distance FROM walking_distances WHERE origin_id = ? AND destination_id = ?''',
                       (origin_id, destination_id,))
        distance_row = cursor.fetchone()

        conn.close()
        return distance_row[0] if distance_row else None

    def update_walking_distance(self, origin_id, destination_id, new_distance, new_duration):
        """
        Updates the walking distance and duration for an existing record.

        Args:
            origin_id (str): ID of the origin location.
            destination_id (str): ID of the destination location.
            new_distance (int): Updated walking distance in meters.
            new_duration (int): Updated walking duration in seconds.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Update record where origin and destination match
        cursor.execute('''UPDATE walking_distances SET distance = ?, duration = ?
                          WHERE origin_id = ? AND destination_id = ?''',
                       (new_distance, new_duration, origin_id, destination_id))

        rows_updated = cursor.rowcount  # Get the number of rows updated

        if rows_updated == 0:
            print(
                f"No walking distance record found for origin: {origin_id} and destination: {destination_id} to update.")
        else:
            print(f"{rows_updated} walking distance record(s) updated successfully.")

        conn.commit()
        conn.close()

    def delete_walking_distance(self, origin_id, destination_id):
        """
        Deletes a walking distance record for a specific origin-destination pair.

        Args:
            origin_id (str): ID of the origin location.
            destination_id (str): ID of the destination location.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Delete record where origin and destination match
        cursor.execute('''DELETE FROM walking_distances WHERE origin_id = ? AND destination_id = ?''',
                       (origin_id, destination_id,))

        rows_deleted = cursor.rowcount  # Get the number of rows deleted

        if rows_deleted == 0:
            print(
                f"No walking distance record found for origin: {origin_id} and destination: {destination_id} to delete.")
        else:
            print(f"{rows_deleted} walking distance record(s) deleted successfully.")

        conn.commit()
        conn.close()

    def get_walking_distances_after_date(self, date_str):
        """
        Fetches all walking distance records inserted after a specified date.

        Args:
            date_str (str): Date string in YYYY-MM-DD format.

        Returns:
            list: List of dictionaries, each representing a walking distance record after the specified date.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Convert date string to datetime object
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid date format provided. Please use YYYY-MM-DD.")
            return []

        # Fetch walking distances after the specified date
        cursor.execute('''SELECT * FROM walking_distances WHERE insertion_time >= ?''', (date_obj,))
        distances = cursor.fetchall()

        conn.close()
        return distances

    def get_walking_distances_by_origin(self, origin_id):
        """
        Fetches all walking distance records where the origin ID matches the provided value.

        Args:
            origin_id (str): ID of the origin location.

        Returns:
            list: List of dictionaries, each representing a walking distance record with the specified origin.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch walking distances with matching origin ID
        cursor.execute('''SELECT * FROM walking_distances WHERE origin_id = ?''', (origin_id,))
        distances = cursor.fetchall()

        conn.close()
        return distances

    def get_walking_distances_by_destination(self, destination_id):
        """
        Fetches all walking distance records where the destination ID matches the provided value.

        Args:
            destination_id (str): ID of the destination location.

        Returns:
            list: List of dictionaries, each representing a walking distance record with the specified destination.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch walking distances with matching destination ID
        cursor.execute('''SELECT * FROM walking_distances WHERE destination_id = ?''', (destination_id,))
        distances = cursor.fetchall()

        conn.close()
        return distances

    def get_most_recent_distances(self, count):
        """
        Fetches the most recent walking distance records, limited by the provided count.

        Args:
            count (int): Maximum number of recent records to retrieve.

        Returns:
            list: List of dictionaries, each representing a recent walking distance record.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Order by insertion time descending and limit by count
        cursor.execute('''SELECT * FROM walking_distances ORDER BY insertion_time DESC LIMIT ?''', (count,))
        distances = cursor.fetchall()

        conn.close()
        return distances


# Example usage:
def main():
    db_name = "database.db"
    routes_db = RoutesDAO(db_name)
    routes_db.create_table()


if __name__ == "__main__":
    main()
