import tensorflow as tf
import keras

from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
# Alt. write this way: model = tf.keras.models.Sequential()

model = Sequential()
layer1 = Dense(5, activation='relu', input_dim=2)
model.add(layer1)
layer2 = Dense(5, activation='relu')
model.add(layer2)
layer3 = Dense(3, activation='softmax')
model.add(layer3)

pass