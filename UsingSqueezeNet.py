import tensorflow as tf

'''
###########################
    Written by Kevin Roy  
###########################
'''


class SqueezeNetModel(object):
    # Model Initialization C:
    def __init__(self, original_dim, resize_dim, output_size):
        self.original_dim = original_dim
        self.resize_dim = resize_dim
        self.output_size = output_size
        pass

    # Random crop and flip
    def random_crop_and_flip(self, float_image):
        crop_image = tf.random_crop(float_image, [self.resize_dim, self.resize_dim, 3])
        update_image = tf.image.random_flip_left_right(crop_image)
        return update_image
