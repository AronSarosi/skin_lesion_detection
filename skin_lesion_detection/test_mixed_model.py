from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Input, Flatten, Dropout, Activation, MaxPooling2D, Conv2D, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import concatenate
import numpy as np
import locale
import os



class Mixed_Model():

    def create_mlp(self, input_dim):
        """
        Create Multi-Layer Perceptron as left_hand fork of mixed neural network for numeric and categorical explanatory variables
        """
        model = Sequential()
        model.add(Dense(8, input_dim=input_dim, activation="relu"))
        model.add(Dense(4, activation="relu"))
        return model

    def create_cnn(self, width, height, depth, filters=(16, 32, 64)):
        """
        Create Convolutional Neural Network as right-hand fork of mixed neural network for pixel data
        """
        # initialize the input shape and channel dimension, assuming TensorFlow/channels-last ordering
        input_shape = (height, width, depth)
        chanDim = -1

        # define the model input
        inputs = Input(shape=inputShape)

        # loop over the number of filters
        for (i, f) in enumerate(filters):
            # if this is the first CONV layer then set the input appropriately
            if i == 0:
                x = inputs
            # add aspects of each CONV interation: CONV => RELU => BN => POOL
            x = Conv2D(f, (3, 3), padding="same")(x)
            x = Activation("relu")(x)
            x = BatchNormalization(axis=chanDim)(x)
            x = MaxPooling2D(pool_size=(2, 2))(x)

        # flatten then FC => RELU => BN => DROPOUT
        x = Flatten()(x)
        x = Dense(16)(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Dropout(0.5)(x)

        # apply another FC layer tto match the number of nodes coming out of the MLP
        x = Dense(4)(x)
        x = Activation("relu")(x)

        # construct the CNN and return model
        model = Model(inputs, x)
        return model


    def merge_compile_models(self, input_dim, width, height, depth, filters=(16, 32, 64))
        """
        Join forks of network to combine models for all data types
        """
        # create the MLP and CNN models
        mlp = models.create_mlp(input_dim)
        cnn = models.create_cnn(width, height, depth, filters=(16, 32, 64))

        # create the input to our final set of layers as the output of both the MLP and CNN
        combinedInput = concatenate([mlp.output, cnn.output])

        # add final FC layer head with 2 dense layers with final layer as the multi-classifier head
        x = Dense(4, activation="relu")(combinedInput)
        x = Dense(1, activation="linear")(x)

        # return final model integrating categorical/numerical data and images into single diagnostic prediction
        model = Model(inputs=[mlp.input, cnn.input], outputs=x)


