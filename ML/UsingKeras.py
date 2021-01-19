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

model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])
'''
# predefined multiclass dataset
train_output = model.fit(data, labels, batch_size=20, epochs=5)
print(train_output.history)
# predefined eval dataset
print(model.evaluate(eval_data, eval_labels))
# 3 new data observations
print('{}'.format(repr(model.predict(new_data))))
'''