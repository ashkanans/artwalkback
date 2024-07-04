import os

from backend.web.dao.artwalk.places_dao import PlacesDAO
from database.config import DB_PATH_PC
from models.predict import predict_path
from utils.data_processing import load_data, preprocess_data


def main():
    start_id = "ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"
    end_id = "ChIJKcGbg2NgLxMRthZkUqDs4M8"
    time_span = 120 * 60

    routes_df, places_df = load_data(DB_PATH_PC)
    routes_df, scaler, encoded_types = preprocess_data(routes_df, places_df)  # Ensure to also get encoded_types from preprocess_data

    # Find the latest model file in the models/models directory
    models_dir = "models/models"
    model_files = [f for f in os.listdir(models_dir) if f.endswith(".h5")]
    latest_model_file = max(model_files, key=lambda x: os.path.getctime(os.path.join(models_dir, x)))
    latest_model_path = os.path.abspath(os.path.join(models_dir, latest_model_file))

    # Select top 100,000 rows with highest rating and userRatingCount
    # routes_df = routes_df.nlargest(100000, ['rating', 'userRatingCount'])

    recommended_path = predict_path(start_id, end_id, time_span, scaler, encoded_types,
                                    latest_model_path)  # Pass encoded_types to predict_path
    print("Recommended path:", recommended_path)
    print(PlacesDAO(DB_PATH_PC).get_display_names_by_ids(recommended_path))

if __name__ == "__main__":
    main()