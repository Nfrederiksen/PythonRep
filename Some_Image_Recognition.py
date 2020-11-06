import tensorflow as tf


# Decode image data from a file in TensorFlow
def decode_image(filename, image_type, resize_shape, channels=0):
        value = tf.io.read_file(filename)

        if image_type == 'png':
            decoded_image = tf.image.decode_png(value, channels=channels)
        elif image_type == 'jpeg':
            decoded_image = tf.image.decode_jpeg(value, channels=channels)
        else:
            decoded_image = tf.image.decode_image(value, channels=channels)

        if resize_shape is not None and image_type in ['png', 'jpeg']:
            decoded_image = tf.image.resize(decoded_image, resize_shape)

        return decoded_image


# Return a dataset created from the image file paths
def get_dataset(image_paths, image_type, resize_shape, channels):
    filename_tensor = tf.constant(image_paths)
    dataset = tf.data.Dataset.from_tensor_slices(filename_tensor)

    def _map_fn(filename):
        return decode_image(filename, image_type, resize_shape, channels=channels)

    return dataset.map(_map_fn)

# Get the decoded image data from the input image file paths
def get_image_data(image_paths, image_type=None, resize_shape=None, channels=0):
    dataset = get_dataset(image_paths, image_type, resize_shape, channels)
    # Make an Iterator for dataset
    iterator = dataset.make_one_shot_iterator()
    # Time to Extract
    next_image = iterator.get_next()
    # return a list of all our image pixel data
    image_data_list = []
    with tf.Session() as sess:
        for i in range(len(image_paths)):
            image_data = sess.run(next_image)
            image_data_list.append(image_data)

    return image_data_list

def sess_playground():
    decoded_image = decode_image('BruceChandling.jpg', 'jpeg', [50, 50], channels=0)
    with tf.compat.v1.Session() as sess:
        print('Original: {}'.format(
            repr(sess.run(decoded_image))))  # Decoded image data
        resized_img = tf.image.resize(decoded_image, (3, 2))
        print('Resized: {}'.format(
            repr(sess.run(resized_img))))


class MNISTModel(object):
    # Model Initialization
    def __init__(self, input_dim, output_size):
        self.input_dim = input_dim
        self.output_size = output_size

    # CNN Layers
    def model_layers(self, inputs, is_training):
        # Convert the input data, inputs, into NHWC format.
        reshaped_inputs = tf.reshape(inputs, [-1, self.input_dim, self.input_dim, 1])
        # Let's Get COnv LAyers! 32 filters - each 5x5 big.
        conv1 = tf.layers.conv2d(reshaped_inputs, 32, [5, 5],
                                 padding='same', activation=tf.nn.relu,
                                 name='conv1')
        pass

sess_playground()
pass

