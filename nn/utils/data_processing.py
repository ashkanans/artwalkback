import sqlite3

import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_data(database_path):
    conn = sqlite3.connect(database_path)

    # Define the values to filter for in the types column
    filter_values = ['historical_landmark', 'landmark', 'museum', 'tourist_attraction']

    # Create a placeholder string for the filter condition
    filter_condition = ' OR '.join([f'types LIKE "%{value}%"' for value in filter_values])

    # Load filtered places data
    places_query = f'''
        SELECT *
        FROM places
        WHERE {filter_condition}
    '''
    places_df = pd.read_sql(places_query, conn)

    # Load routes data
    routes_query = '''
        SELECT r.originId, r.destId, r.distanceMeters, r.duration, r.created_at, p.rating, p.userRatingCount, p.types
        FROM routes r
        JOIN places p ON r.destId = p.id
        WHERE r.originId IS NOT NULL
        AND r.destId IS NOT NULL
        AND r.distanceMeters IS NOT NULL
        AND r.duration IS NOT NULL
        AND r.created_at IS NOT NULL
        AND p.rating IS NOT NULL
        AND p.userRatingCount IS NOT NULL
        AND p.types IS NOT NULL
    '''
    routes_df = pd.read_sql(routes_query, conn)

    conn.close()

    # Filter routes_df to only include routes with originId and destId in the filtered places_df
    filtered_origin_ids = places_df['id'].tolist()
    filtered_dest_ids = places_df['id'].tolist()
    routes_df = routes_df[routes_df['originId'].isin(filtered_origin_ids) & routes_df['destId'].isin(filtered_dest_ids)]

    return routes_df, places_df

def preprocess_data(routes_df, places_df):
    # Convert duration to minutes
    routes_df['durationMinutes'] = routes_df['duration'].apply(lambda x:
                                                               int(x.split()[0]) if x and 'min' in x else (
                                                                   int(x.split()[0]) * 60 if x else None))

    # Drop rows with None values in durationMinutes
    routes_df = routes_df.dropna(subset=['durationMinutes'])

    # Normalize numerical features
    scaler = StandardScaler()
    numerical_features = ['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']
    routes_df[numerical_features] = scaler.fit_transform(routes_df[numerical_features])

    # Encode categorical feature 'types' using one-hot encoding
    encoded_types = pd.get_dummies(places_df['types'].apply(lambda x: x.split(', ')).explode()).groupby(level=0).sum()

    encoded_types.index = encoded_types.index.astype(str)

    routes_df = pd.merge(routes_df, encoded_types, left_on='destId', right_index=True, how='left')

    # Fill NaN values in encoded types (if any)
    routes_df[encoded_types.columns] = routes_df[encoded_types.columns].fillna(0)

    # Select relevant features for training
    features = numerical_features + list(encoded_types.columns)

    return routes_df[features], scaler, encoded_types
