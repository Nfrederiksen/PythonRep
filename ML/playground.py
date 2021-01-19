import tensorflow as tf
import numpy as np


def init_inputs(input_size):
    inputs = tf.placeholder(tf.float32, shape=(None, input_size), name='inputs')
    print('I used tf.placeholder Nice!')
    return inputs


def init_labels(output_size):
    labels = tf.placeholder(tf.int32, shape=(None, output_size), name='labels')
    return labels


def model_layers(inputs, output_size):
    logits = tf.layers.dense(inputs, output_size, name='logits')
    return logits
    pass


def get_accuracy(logits, labels):
    # Get the odds.
    probs = tf.nn.sigmoid(logits)
    # Get the odds as either 1 or 0.
    rounded_probs = tf.round(probs)
    # Does not match labels, convert it.
    predictions = tf.cast(rounded_probs, tf.int32)
    # Let's find the accuracy in the predictions with the labels.
    is_correct = tf.equal(predictions, labels)
    # Since we now want the mean we have to convert back to float32, rn they're True/False
    is_correct_float = tf.cast(is_correct, tf.float32)
    # Let's see how accurate it is, and find that mean correctness.
    accuracy = tf.reduce_mean(is_correct_float)

    return accuracy


def optimize_loss(logits, labels):
    # To get our loss parameter, we need labels to be in floats
    labels_float = tf.cast(labels, tf.float32)
    # Find cross entropy between labels and logits!
    cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels_float, logits=logits)
    # loss should be a single value, cro_ent is a sigmoid for every label.
    # so we say that the loss is the mean cross entropy.
    loss = tf.reduce_mean(cross_entropy)
    # Now let's optimize. Choose an Optimizer object (Adam in this case, he got good default learning rate etc.)
    adam = tf.train.AdamOptimizer()
    train_op = adam.minimize(loss)

    pass
