from telnetlib import SE
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web

import datetime as dt
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.models import Sequential


token1 = 'BTC'
against1 = "USD"

start = dt.datetime(2020, 1, 1)
end = dt.datetime.now()

data = web.DataReader(f'{token1}-{against1}', 'yahoo', start, end)

# prepare data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

# predictionDays_10 = 10
# predictionYear = 365

prediction1 = 20

x_train, y_train = [], []

for x in range(prediction1, len(scaled_data)):
    x_train.append(scaled_data[x-prediction1: x,0])
    y_train.append(scaled_data[x,0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

print (x_train, y_train)

# Create Neural Network

model = Sequential()

model.add(LSTM(units = 50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units = 50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units = 50))
model.add(Dropout(0.2))

model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss='mean_squared_error')

model.fit(x_train, y_train, epochs=25, batch_size = 32)

#testing the model
test_start = dt.datetime(2020, 1, 1)
test_end = dt.datetime.now()

test_data = web.DataReader(f'{token1}-{against1}', 'yahoo', test_start, test_end)

actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction1:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.fit_transform(model_inputs)

x_test = []

for x in range(prediction1, len(model_inputs)):
    x_test.append(model_inputs[x-prediction1:x, 0])

x_test =  np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

plt.plot(actual_prices, color='black', label='Actual Prices')
plt.plot(prediction1, color='green', label='PredictionPries')

plt.title(f'{token1} price prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()



