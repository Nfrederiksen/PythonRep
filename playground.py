import tensorflow as tf

def init_inputs(input_size):
    inputs = tf.placeholder(tf.float32, shape=(None, input_size), name='inputs')
    print('I used tf.placeholder Nice!')
    return inputs

def init_labels(output_size):
    labels = tf.placeholder(tf.int32, shape=(None, output_size), name='labels')
    return labels
    pass

