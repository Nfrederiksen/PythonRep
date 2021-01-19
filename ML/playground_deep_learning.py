import tensorflow as tf

'''
###########################
    Written by Kevin Roy  
###########################
'''

import numpy as np


def sigmoid(x):  # sigmoid activation function
    """The sigmoid activation function on the input x"""
    return 1 / (1 + np.exp(-x))


def forward_propagation(input_data, weights, bias):
    """
     Computes the forward propagation operation of a perceptron and
     returns the output after applying the sigmoid activation function
    """
    # take the dot product of input and weight and add the bias
    return sigmoid(np.dot(input_data, weights) + bias)  # the perceptron equation


def calculate_error(Y, Y_predicted):
    """Computes the binary cross entropy error"""
    # the cross entropy error
    return - Y * np.log(Y_predicted) - (1 - Y) * np.log(1 - Y_predicted)


def gradient(target, actual, X):
    """"Gradient of weights and bias"""
    dW = - (target - actual) * X  # gradient of weights
    db = target - actual  # gradient of bias
    return dW, db


def update_parameters(W, b, dW, db, learning_rate):
    """Updating the weights and bias value"""
    W = W - dW * learning_rate  # update weight
    b = b - db * learning_rate  # update learning rate
    return W, b


def train(X, Y, weights, bias, epochs, learning_rate):
    """Training the perceptron using stochastic update"""
    sum_error = 0.0
    for i in range(epochs):  # outer loop iterates epoch times
        for j in range(len(X)):  # inner loop iterates length of X times
            Y_predicted = forward_propagation(X[j], weights.T, bias)  # predicted label
            sum_error = sum_error + calculate_error(Y[j], Y_predicted)  # compute error
            dW, db = gradient(Y[j], Y_predicted, X[j])  # find gradient
            weights, bias = update_parameters(weights, bias, dW, db, learning_rate)  # update parameters
        print("epochs:", i, "error:", sum_error)
        sum_error = 0  # re-intialize sum error at the end of each epoch
    return weights, bias


# Initialize parameters
# declaring two data points
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

Y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # actual label
weights = np.array([0.0, 0.0])  # weights of perceptron
bias = 0.0  # bias value
learning_rate = 0.1  # learning rate
epochs = 10  # set epochs
print("Before training")
print("weights:", weights, "bias:", bias)

weights, bias = train(X, Y, weights, bias, epochs, learning_rate)  # train the function

print("\nAfter training")
print("weights:", weights, "bias:", bias)
# Predict values
predicted_labels = forward_propagation(X, weights.T, bias)
print("Target labels:  ", Y)
print("Predicted label:", (predicted_labels > 0.5) * 1)