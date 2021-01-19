import numpy as np
from matplotlib import pyplot as plt


def sigmoid(z):
    """sigmoid activation function on input z"""
    return 1 / (1 + np.exp(-z))  # defines the sigmoid activation function


def forward_propagation(X, Y, W1, b1, W2, b2):
    """
     Computes the forward propagation operation of a neural network and
     returns the output after applying the sigmoid activation function
    """
    net_h = np.dot(W1, X) + b1  # net output at the hidden layer
    out_h = sigmoid(net_h)  # actual after applying sigmoid
    net_y = np.dot(W2, out_h) + b2  # net output at the output layer
    out_y = sigmoid(net_y)  # actual output at the output layer

    return out_h, out_y


def calculate_error(y, y_predicted):
    """Computes cross entropy error"""
    loss = np.sum(- y * np.log(y_predicted) - (1 - y) * np.log(1 - y_predicted))
    return loss


def backward_propagation(X, Y, out_h, out_y, W2):
    """
     Computes the backpropagation operation of a neural network and
     returns the derivative of weights and biases
    """
    l2_error = out_y - Y  # actual - target
    dW2 = np.dot(l2_error,
                 out_h.T)  # derivative of layer 2 weights is the dot product of error at layer 2 and hidden layer output
    db2 = np.sum(l2_error, axis=1, keepdims=True)  # derivative of layer 2 bias  is simply the error at layer 2

    dh = np.dot(W2.T, l2_error)  # compute dot product of weights in layer 2 with error at layer 2
    l1_error = np.multiply(dh, out_h * (1 - out_h))  # compute layer 1 error
    dW1 = np.dot(l1_error, X.T)  # derivative of layer 2 weights is the dot product of error at layer 1 and input
    db1 = np.sum(l1_error, axis=1, keepdims=True)  # derivative of layer 1 bias  is simply the error at layer 1

    return dW1, db1, dW2, db2  # return the derivatives of parameters


def update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate):
    """Updates weights and biases and returns thir values"""
    W1 = W1 - learning_rate * dW1
    W2 = W2 - learning_rate * dW2
    b1 = b1 - learning_rate * db1
    b2 = b2 - learning_rate * db2
    return W1, b1, W2, b2


def train(X, Y, W1, b1, W2, b2, num_iterations, losses, learning_rate):
    """Trains the neural network and returns updated weights, bias and loss"""
    for i in range(num_iterations):
        A1, A2 = forward_propagation(X, Y, W1, b1, W2, b2)
        losses[i, 0] = calculate_error(Y, A2)
        dW1, db1, dW2, db2 = backward_propagation(X, Y, A1, A2, W2)
        W1, b1, W2, b2 = update_parameters(W1, b1, W2, b2, dW1, db1, dW2, db2, learning_rate)
    return W1, b1, W2, b2, losses


np.random.seed(42)  # seed function to generate the same random value

# Initializing parameters
X = np.array([[0, 0, 1, 1], [0, 1, 0, 1]])
Y = np.array([[0, 1, 1, 0]])  # XOR
n_h = 2
n_x = X.shape[0]
n_y = Y.shape[0]
W1 = np.random.randn(n_h, n_x)
b1 = np.zeros((n_h, 1))
W2 = np.random.randn(n_y, n_h)
b2 = np.zeros((n_y, 1))

num_iterations = 100000
learning_rate = 0.01
losses = np.zeros((num_iterations, 1))

W1, b1, W2, b2, losses = train(X, Y, W1, b1, W2, b2, num_iterations, losses, learning_rate)
print("After training:\n")
print("W1:\n", W1)
print("b1:\n", b1)
print("W2:\n", W2)
print("b2:\n", b2)
print("losses:\n", losses)

# Evaluating the performance
plt.figure()
plt.plot(losses)
plt.xlabel("EPOCHS")
plt.ylabel("Loss value")
plt.show()
plt.savefig('output/legend.png')

X2 = np.array([[1, 1, 0, 0], [0, 1, 0, 1]])
Y2 = np.array([[1, 0, 0, 1]])  # XOR
# Predicting value
A1, A2 = forward_propagation(X2, Y2, W1, b1, W2, b2)
pred = (A2 > 0.5) * 1.0
print("Predicted labels:", pred)
