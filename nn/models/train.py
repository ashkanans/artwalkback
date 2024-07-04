import datetime

from sklearn.model_selection import ParameterGrid

from nn.database.config import DB_PATH_PC
from nn.models.model import create_model
from nn.utils.data_processing import load_data, preprocess_data
from nn.utils.feature_engineering import generate_training_data



def main():
    # Load and preprocess data
    routes_df, places_df = load_data(DB_PATH_PC)
    routes_df, scaler, encoded_types = preprocess_data(routes_df, places_df)

    # Generate training data
    X, y = generate_training_data(routes_df, encoded_types, sequence_length=10)

    # Define a list of hyperparameters to loop through
    param_grid = {
        'lstm_units': [50, 100, 150],
        'dropout_rate': [0.2, 0.3, 0.4],
        'learning_rate': [0.001, 0.01, 0.1],
        'epochs': [50, 100],
        'batch_size': [64, 128],
        'validation_split': [0.2, 0.3]
    }

    # Total number of combinations
    total_combinations = len(list(ParameterGrid(param_grid)))
    current_combination = 0

    # Loop through each combination of hyperparameters
    for params in ParameterGrid(param_grid):
        current_combination += 1
        print(f"Training combination {current_combination}/{total_combinations}:")
        print(f"Hyperparameters: {params}")

        # Create model with current set of hyperparameters
        model = create_model(input_dim=X.shape[2], num_features=y.shape[1], lstm_units=params['lstm_units'],
                             dropout_rate=params['dropout_rate'], learning_rate=params['learning_rate'])

        # Train the model
        print("Training model...")
        model.fit(X, y, epochs=params['epochs'], batch_size=params['batch_size'],
                  validation_split=params['validation_split'], verbose=1)

        # Save the model with a name reflecting the hyperparameters
        model_name = f'tour_guide_model_lstm{params["lstm_units"]}_dropout{params["dropout_rate"]}_lr{params["learning_rate"]}_epochs{params["epochs"]}_batch{params["batch_size"]}_valsplit{params["validation_split"]}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.h5'
        model.save(f'models/{model_name}')

        print(f"Model saved as {model_name}")
        print()

if __name__ == "__main__":
    main()