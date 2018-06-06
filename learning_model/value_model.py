from __future__ import print_function

import datetime
import os

import numpy as np

import keras
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.optimizers import RMSprop
from keras.layers.normalization import BatchNormalization


class ValueModel:
    WIDTH = 8
    HEIGHT = 8

    BATCH_SIZE = 128
    EPOCHS = 5

    def __init__(self):
        self.model = self.build()

    # Training
    def build(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', input_shape=[self.WIDTH, self.HEIGHT, 1]))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Conv2D(32, (3, 3), padding='same', input_shape=[self.WIDTH, self.HEIGHT, 1]))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(32, (3, 3)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Conv2D(32, (3, 3), padding='same', input_shape=[self.WIDTH, self.HEIGHT, 1]))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(128))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        keras.optimizers.RMSprop(lr=0.001)
        model.compile(loss='mean_squared_error',
                      optimizer=RMSprop(),
                      metrics=["accuracy"])
        return model

    def train(self, data):
        features = np.array([np.array(map) for map in data[0]])
        labels = np.array([reward for reward in data[1]])
        self._train(features.reshape(len(features), self.HEIGHT, self.WIDTH, 1), labels)

    def _train(self, feature, labels):
        history = self.model.fit(feature, labels,
                                 batch_size=self.BATCH_SIZE,
                                 epochs=self.EPOCHS,
                                 verbose=0,
                                 validation_data=(feature, labels))

    def value_maps(self, data):
        maps = np.array([np.array(m) for m in data])
        return self._test(maps)

    def _test(self, feature):
        return self.model.predict(feature.reshape(len(feature), self.HEIGHT, self.WIDTH, 1))

    def save_model(self):
        if not os.path.exists("models"):
            os.makedirs("models")
        filename = "models/model" + str(datetime.datetime.now()).replace(":", "").replace(".", "").replace(" ", "")
        model_json = self.model.to_json()
        with open(filename, "w") as file:
            file.write(model_json)
        self.model.save_weights(filename + ".h5")
