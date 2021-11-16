from keras import Model
from keras.layers import *


class Fiber_Photometry_Model:
    def __init__(self, window_size, learning_rate):
        self.enc_model = None
        self.model = None
        self.window_size = window_size
        self.lr = learning_rate

    def build_dense_model(self, compression):
        enc_input = Input((self.window_size,))
        dense = Dense(self.window_size)(enc_input)
        dense = Dense(self.window_size * 2)(dense)
        dense = Dense(self.window_size * 3)(dense)
        dense = Dense(self.window_size * 2)(dense)
        dense = Dense(self.window_size)(dense)
        enc_out = Dense(compression)(dense)
        dec_input = Dense(compression)(enc_out)
        dense = Dense(self.window_size)(dense)
        dense = Dense(self.window_size * 2)(dec_input)
        dense = Dense(self.window_size * 3)(dense)
        dense = Dense(self.window_size * 2)(dense)
        dec_out = Dense(self.window_size)(dense)

        self.enc_model = Model(inputs=[enc_input], outputs=[enc_out], name='Encoder Model')
        self.model = Model(inputs=[enc_input], outputs=[dec_out], name='Autoencoder Model')

    @property
    def summary(self):
        print(self.model.summary())
        print(self.enc_model.summary())
