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

        return decoded_image


def sess_playground():
    decoded_image = decode_image('BruceChandling.jpg', 'jpeg', [50, 50], channels=0)
    with tf.compat.v1.Session() as sess:
        print('Original: {}'.format(
            repr(sess.run(decoded_image))))  # Decoded image data
        resized_img = tf.image.resize_images(decoded_image, (3, 2))
        print('Resized: {}'.format(
            repr(sess.run(resized_img))))

sess_playground()
pass

