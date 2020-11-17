import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense



# read in training data
train_data = pd.read_csv("train.csv")
# read the test data
test_data = pd.read_csv("test.csv")
# fill in missing values with 0
train_data.fillna(0, inplace=True)
test_data.fillna(0, inplace=True)
# drop unuseful features
train_X = train_data.drop(["PassengerId", "Name", "Cabin", "Embarked", "Ticket", "Fare", "Survived"], axis=1)
test_X = test_data.drop(["PassengerId", "Name", "Cabin", "Embarked", "Ticket", "Fare", "Survived"], axis=1)
# assign an integer value of gender
def assign_gender_integer(row):
	if row['Gender'] == 'male':
		return 1
	else:
		return 0

# call the assign_gender_integer method to assign 1 to male and 0 to female
train_X['Gender'] = train_X.apply(assign_gender_integer, axis=1)
test_X['Gender'] = test_X.apply(assign_gender_integer, axis=1)
#print("Features\n:", train_X)

# get the label
train_y = train_data["Survived"]
test_y = test_data["Survived"]
#print("Labels\n:", train_y)

# [Step 2] USING SEQUENTIAL
# get number of columns in training data
n_cols = train_X.shape[1]

# model for a binary classification to predict survival
model = Sequential()
# add a hidden layer with 32 nodes
model.add(Dense(32, activation='relu', input_shape=(n_cols,)))
# add a hidden layer with 64 nodes
model.add(Dense(64, activation='relu'))

# add the output layer with the sigmoid activation function
model.add(Dense(1, activation='sigmoid'))

# -- view model summary --
# model.summary()

# [Step 3] compile the model
print("Compiling model for a binary classification task")
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Succeeded")
# fit the model [Step 4]
model.fit(train_X, train_y, epochs=20, batch_size=30, verbose=1)
# model.save("titanic_model.h5")

# [Step 4] evaluate the keras model on training data
_, accuracy = model.evaluate(train_X, train_y)
print('Accuracy: %.2f' % (accuracy * 100))


model_loaded = load_model("titanic_model.h5")
# [Step 5] predict the output
predictions = model_loaded.predict(test_X)
# -- view model summary --
# model_loaded.summary()

# evaluate model's performance on test data
_, accuracy = model_loaded.evaluate(test_X, test_y)
print('Accuracy on Test: %.2f' % (accuracy * 100))


