import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    """The sigmoid activation function on the input x"""
    return 1 / (1 + np.exp(-z))

def forward_propagation(X, W, b):
    """
     Computes the forward propagation operation of a perceptron and
     returns the output after applying the sigmoid activation function
    """
    weighted_sum = np.dot(X, W) + b # calculate the weighted sum of X and W
    prediction = sigmoid(weighted_sum) # apply the sigmoid activation function
    return prediction


def calculate_error(y, y_predicted):
   """Computes the binary cross entropy error"""
   loss = np.sum(- y * np.log(y_predicted) - (1 - y) * np.log(1 - y_predicted)) # calculate error
   return loss

def gradient(X, Y, Y_predicted):
    """"Gradient of weights and bias"""
    Error = Y_predicted - Y # Calculate error
    dW = np.dot(X.T, Error) # Compute derivative of error w.r.t weight, i.e., (target - output) * x
    db = np.sum(Error) # Compute derivative of error w.r.t bias
    return dW, db # return derivative of weight and bias

def update_parameters(W, b, dW, db, learning_rate):
    """Updating the weights and bias value"""
    W = W - learning_rate * dW # update weight
    b = b - learning_rate * db # update bias
    return W, b # return weight and bias


def train(X, Y, learning_rate, W, b, epochs, losses):
    """Training the perceptron using batch update"""
    for i in range(epochs): # loop over the total epochs
        Y_predicted = forward_propagation(X, W, b) # compute forward pass
        losses[i, 0] = calculate_error(Y, Y_predicted) # calculate error
        dW, db = gradient(X, Y, Y_predicted) # calculate gradient
        W, b = update_parameters(W, b, dW, db, learning_rate) # update parameters

    return W, b, losses

# Initialize parameters
# features
X = np.array(
   [[2.78, 2.55],
	[1.46, 2.36],
	[3.39, 4.40],
	[1.38, 1.85],
	[3.06, 3.00],
	[7.62, 2.75],
	[5.33, 2.08],
	[6.92, 1.77],
	[8.67, -0.24],
	[7.67, 3.50]])

Y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]) # target label
weights = np.array([0.0, 0.0]) # weights of perceptron
bias = 0.0 # bias value
epochs = 10000 # total epochs
learning_rate = 0.01 # learning rate
losses = np.zeros((epochs, 1)) # compute loss
print("Before training")
print("weights:", weights, "bias:", bias)
print("Target labels:", Y)
W, b, losses = train(X, Y, learning_rate, weights, bias, epochs, losses)

# Evaluating the performance
plt.figure()
plt.plot(losses)
plt.xlabel("EPOCHS")
plt.ylabel("Loss value")
plt.show()
plt.savefig('output/legend.png')

print("\nAfter training")
print("weights:", W, "bias:", b)
# Predict value
A2 = forward_propagation(X, W, b)
pred = (A2 > 0.5) * 1

print("Predicted labels:", pred)