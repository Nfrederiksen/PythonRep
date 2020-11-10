import tensorflow as tf
import math

block_layer_sizes = {
    18: [2, 2, 2, 2],
    34: [3, 4, 6, 3],
    50: [3, 4, 6, 3],
    101: [3, 4, 23, 3],
    152: [3, 8, 36, 3],
    200: [3, 24, 36, 3]
}

class ResNetModel(object):
    # Model Initialization
    def __init__(self, min_aspect_dim, resize_dim, num_layers, output_size, data_format='channels_last'):
        self.min_aspect_dim = min_aspect_dim
        self.resize_dim = resize_dim
        self.filters_initial = 64
        self.block_strides = [1, 2, 2, 2]
        self.data_format = data_format
        self.output_size = output_size
        self.block_layer_sizes = block_layer_sizes[num_layers]
        self.bottleneck = num_layers >= 50 # True or False


    # Custom padding function
    def custom_padding(self, inputs, kernel_size):
        # CODE HERE
        pad_total = kernel_size - 1
        pad_before = pad_total // 2
        pad_after = pad_total - pad_before
        if self.data_format == 'channels_first':
            padded_inputs = tf.pad(inputs, [[0, 0], [0, 0], [pad_before, pad_after], [pad_before, pad_after]])
        else:
            padded_inputs = tf.pad(inputs, [[0, 0], [pad_before, pad_after], [pad_before, pad_after], [0, 0]])

        return padded_inputs

    # Custom convolution function w/ consistent padding
    def custom_conv2d(self, inputs, filters, kernel_size, strides, name=None):
        if strides > 1:
            padding = 'valid'
            inputs = self.custom_padding(inputs, kernel_size)
        else:
            padding = 'same'
        return tf.layers.conv2d(
            inputs=inputs, filters=filters, kernel_size=kernel_size,
            strides=strides, padding=padding, data_format=self.data_format,
            name=name)

        # Apply pre-activation to input data

    def pre_activation(self, inputs, is_training):
        axis = 1 if self.data_format == 'channels_first' else 3
        bn_inputs = tf.layers.batch_normalization(inputs, axis=axis, training=is_training)
        pre_activated_inputs = tf.nn.relu(bn_inputs)
        return pre_activated_inputs

    # Returns pre-activated inputs and the shortcut
    def pre_activation_with_shortcut(self, inputs, is_training, shortcut_params):
        pre_activated_inputs = self.pre_activation(inputs, is_training)
        shortcut = inputs
        shortcut_filters = shortcut_params[0]
        if shortcut_filters is not None:
            strides = shortcut_params[1]
            shortcut = self.custom_conv2d(pre_activated_inputs, shortcut_filters, kernel_size=1, strides=strides)

        return pre_activated_inputs, shortcut
        # ResNet building block

    def regular_block(self, inputs, filters, strides, is_training, index, shortcut_filters=None):
        with tf.variable_scope('regular_block{}'.format(index)):
            shortcut_params = (shortcut_filters, strides)
            pre_activated1, shortcut = self.pre_activation_with_shortcut(inputs, is_training, shortcut_params)
            conv1 = self.custom_conv2d(pre_activated1, filters, 3, strides)
            #
            pre_activated2 = self.pre_activation(conv1, is_training)
            conv2 = self.custom_conv2d(pre_activated2, filters=filters, kernel_size=3, strides=1)
            return conv2 + shortcut
    # ResNet bottleneck block
    def bottleneck_block(self, inputs, filters, strides, is_training, index, shortcut_filters=None):
        with tf.variable_scope('bottleneck_block{}'.format(index)):
            shortcut_params = (shortcut_filters, strides)
            pre_activated1, shortcut = self.pre_activation_with_shortcut(inputs, is_training, shortcut_params)
            conv1 = self.custom_conv2d(pre_activated1, filters, 1, 1)
            pre_activated2 = self.pre_activation(conv1, is_training)
            conv2 = self.custom_conv2d(pre_activated2, filters, 3, strides)
            # CODE HERE
            pre_activated3 = self.pre_activation(conv2, is_training)
            conv3 = self.custom_conv2d(pre_activated3, filters*4, 1, 1)
            return conv3 + shortcut
    # Creates a layer of blocks
    def block_layer(self, inputs, filters, strides, num_blocks, is_training, index):
        with tf.variable_scope('block_layer{}'.format(index)):
            shortcut_filters = 4 * filters if self.bottleneck else filters
            block_fn = self.bottleneck_block if self.bottleneck else self.regular_block
            block_output = block_fn(inputs, filters, strides, is_training, 0,
                                    shortcut_filters=shortcut_filters)
            # stack the blocks in this layer
            for i in range(1, num_blocks):
                block_output = block_fn(block_output, filters, 1, is_training, i)
            return block_output