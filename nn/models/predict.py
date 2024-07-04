import sqlite3

import numpy as np
import pandas as pd
from keras.src.saving import load_model

from nn.database.config import DB_PATH_PC


def predict_path(start_id, end_id, time_span, scaler, encoded_types, model_path):
    model = load_model(model_path)

    conn = sqlite3.connect(
        DB_PATH_PC)
    # Define the values to filter for in the types column
    filter_values = ['historical_landmark', 'landmark', 'museum', 'tourist_attraction']

    # Create a placeholder string for the filter condition
    filter_condition = ' OR '.join([f'p.types LIKE "%{value}%"' for value in filter_values])

    # Construct the SQL query with the filter condition
    query = f'''
        SELECT r.originId, r.destId, r.distanceMeters, r.duration, r.created_at, p.rating, p.userRatingCount, p.types
        FROM routes r
        JOIN places p ON r.destId = p.id
        WHERE r.originId = ?
        AND ({filter_condition})
    '''

    path = [start_id]
    current_time = 0

    while current_time < time_span:
        df = pd.read_sql(query, conn, params=(start_id,))

        if df.empty:
            break

        df['durationMinutes'] = df['duration'].apply(lambda x:
                                                     int(x.split()[0]) if x and 'min' in x else (
                                                         int(x.split()[0]) * 60 if x else None))

        df = df.dropna(subset=['durationMinutes'])

        # Apply the same scaler to numerical features
        df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']] = scaler.transform(
            df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']])

        # Ensure all expected type columns are present
        type_columns = list(encoded_types.columns)
        for col in type_columns:
            if col not in df.columns:
                df[col] = 0

        # Prepare input data X with shape (1, None, number_of_features)
        feature_columns = ['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount'] + list(encoded_types.columns)
        X = np.array(df[feature_columns].values)
        X = np.expand_dims(X, axis=0)  # Add batch dimension
        X = np.swapaxes(X, 0, 1)  # Swap axis to (None, 1, number_of_features) assuming predicting for a single sequence

        # Predict probabilities
        pred_probs = model.predict(X)

        # Ensure dimensions match
        if len(pred_probs) != len(df):
            raise ValueError(f"Length of pred_probs ({len(pred_probs)}) does not match length of DataFrame ({len(df)})")

        # Find the next best location that is not already in path
        next_location = None
        for index, row in df.iterrows():
            if row['destId'] not in path:
                next_location = row
                break

        if next_location is None:
            break  # If no valid next location found, break out of the loop

        # Add next_location to path
        path.append(next_location['destId'])
        current_time += int(next_location['duration'])

        # Update the origin for the next prediction
        start_id = next_location['destId']

    conn.close()
    return path