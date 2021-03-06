import numpy as np
import pandas
import time

class Sigmoid:
    def __init__(self):
        pass

    def forward(self, input):
        sigmoid_grad = 1.0/(1 + np.exp(-input))
        return sigmoid_grad

    def backward(self, input, grad_output):
        sigmoid_grad = self.forward(input)
        return sigmoid_grad * (1 - sigmoid_grad) * grad_output


class Dense:
    def __init__(self, input_units, output_units, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.weights = np.zeros((input_units, output_units))
        self.biases = np.zeros(output_units)

    def forward(self, input):
        return np.dot(input, self.weights) + self.biases

    def backward(self, input, grad_output):
        # weights = [input units, output units]
        # grad_output = [batch size, output units]
        # input = [batch size, input units]
        grad_input = np.dot(grad_output, self.weights.T)
        grad_weights = np.dot(input.T, grad_output)
        grad_biases = np.mean(grad_output, axis=0)
        assert grad_weights.shape == self.weights.shape
        self.weights = self.weights - self.learning_rate * grad_weights
        self.biases = self.biases - self.learning_rate * grad_biases
        return grad_input


def mean_squared_error(prediction, label):
    error = 0
    for i in range(len(prediction)):
        error += (prediction[i] - label[i]) ** 2
    return error / len(prediction)


def grad_mean_squared_error(prediction, label):
    grad = []
    for i in range(len(prediction)):
        grad.append((prediction[i] - label[i]) * 2 / len(prediction))
    return np.asarray(grad)

start_time = time.time()
train_file = "../data/subdata.csv"
training_data = pandas.read_csv(train_file)
y_train = training_data.Class
y_train = np.asarray(y_train)
training_data = training_data.drop(['Class'], axis=1)
X_train = np.asarray(training_data)
training_count = len(X_train[:, 0])

network = [Dense(X_train.shape[1], 50), Sigmoid(), Dense(50, 50), Sigmoid(), Dense(50, 1)]


def forward(network, X):
    activations = []
    input = X
    # Looping through each layer
    for l in network:
        activations.append(l.forward(input))
        # Updating input to last layer output
        input = activations[-1]

    assert len(activations) == len(network)
    return activations


def predict(network, X):
    # Compute network predictions. Returning indices of largest Logit probability
    logits = forward(network, X)[-1]
    return logits.argmax(axis=-1)


def train(network, X, y):
    # Train our network on a given batch of X and y.
    # We first need to run forward to get all layer activations.
    # Then we can run layer.backward going from last to first layer.
    # After we have called backward for all layers, all Dense layers have already made one gradient step.

    # Get the layer activations
    layer_activations = forward(network, X)
    layer_inputs = [X] + layer_activations  # layer_input[i] is an input for network[i]
    logits = layer_activations[-1]

    # Compute the loss and the initial gradient
    predictions = []
    for each in logits:
        if each[0] >= 0.5:
            predictions.append(1)
        else:
            predictions.append(0)
    loss = mean_squared_error(predictions, y)
    loss_grad = grad_mean_squared_error(logits, y)

    # Propagate gradients through the network
    # Reverse propogation as this is backprop
    for layer_index in range(len(network))[::-1]:
        layer = network[layer_index]
        loss_grad = layer.backward(layer_inputs[layer_index], loss_grad)
    return np.mean(loss)


train_log = []
batch_size = 32
for epoch in range(1):
    for start_idx in range(0, len(X_train) - batch_size + 1, batch_size):
        x_batch = X_train[start_idx:start_idx+batch_size]
        y_batch = y_train[start_idx:start_idx+batch_size]
        train(network, x_batch, y_batch)
    train_log.append(np.mean(predict(network, X_train) == y_train))
    print("Epoch", epoch)
    print("Train accuracy:", train_log[-1])

end_time = time.time()
print(end_time - start_time)
