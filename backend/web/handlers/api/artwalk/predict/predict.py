import os

from backend.database_config.database_artwalk.config import DB_PATH
from backend.tests.api.AWBaseTestCase import ArtWalkBaseAPITestCase
from backend.web.dao.artwalk.places_dao import PlacesDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from nn.models.predict import predict_path
from nn.utils.data_processing import load_data, preprocess_data
from web_app import app


class ArtwalkPredictHandler:
    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        try:
            start_id = request.args.get('start_id', 'ChIJ1UCDJ1NgLxMRtrsCzOHxdvY')
            end_id = request.args.get('end_id', 'ChIJKcGbg2NgLxMRthZkUqDs4M8')
            time_span = int(request.args.get('time_span', 120 * 60))

            # Load and preprocess data
            db_path = DB_PATH
            routes_df, places_df = load_data(db_path)
            routes_df, scaler, encoded_types = preprocess_data(routes_df, places_df)

            # Find the latest model file
            models_dir = "E:\\EDU\\MACC\\artwalkback\\nn\\models\\models"
            model_files = [f for f in os.listdir(models_dir) if f.endswith(".h5")]
            latest_model_file = max(model_files, key=lambda x: os.path.getctime(os.path.join(models_dir, x)))
            latest_model_path = os.path.abspath(os.path.join(models_dir, latest_model_file))

            # Predict the recommended path
            recommended_path = predict_path(start_id, end_id, time_span, scaler, encoded_types, latest_model_path)
            display_names = PlacesDAO(db_path).get_display_names_by_ids(recommended_path)

            self.response = {"recommended_path": recommended_path, "display_names": display_names}
            return self.response

        except Exception as e:
            self.response = MESSAGES['LOGIN']['ERROR_CHECKING_CREDENTIALS'](e)
            return self.response
