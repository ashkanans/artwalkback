from keras import Sequential
from keras.src.layers import LSTM, Dense, Dropout
from keras.src.optimizers import Adam


def create_model(input_dim, num_features, lstm_units=50, dropout_rate=0.2, learning_rate=0.001):
    model = Sequential()
    model.add(LSTM(lstm_units, activation='relu', input_shape=(None, input_dim)))
    model.add(Dropout(dropout_rate))
    model.add(Dense(num_features, activation='linear'))  # Output layer for numerical features with linear activation

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')  # Use mean squared error for regression
    return model