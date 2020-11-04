import tensorflow as tf

def init_inputs(input_size):
    inputs=tf.placeholder(tf.float32, shape=(None,input_size), name='inputs')
    print('I used tf.placeholder Nice!')
    return inputs

    pass