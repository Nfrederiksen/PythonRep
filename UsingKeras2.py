import pandas as pd

# read in training data
train_data = pd.read_csv("train.csv")

# fill in missing values with 0
train_data.fillna(0, inplace=True)

# drop unuseful features
train_X = train_data.drop(["PassengerId", "Name", "Cabin", "Embarked", "Ticket", "Fare", "Survived"], axis=1)

# assign an integer value of gender
def assign_gender_integer(row):
	if row['Gender'] == 'male':
		return 1
	else:
		return 0

# call the assign_gender_integer method to assign 1 to male and 0 to female
train_X['Gender'] = train_X.apply(assign_gender_integer, axis=1)
print("Features\n:", train_X)

# get the label
train_y = train_data["Survived"]
print("Labels\n:", train_y)