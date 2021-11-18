from keras import Model
from keras.layers import *
from keras.utils.vis_utils import plot_model


class Fiber_Photometry_Model:
    def __init__(self, window_size, learning_rate):
        self.enc_model = None
        self.model = None
        self.window_size = window_size
        self.lr = learning_rate

    def build_dense_model(self, compression, dropout_amount):
        enc_input = Input((self.window_size,))
        dense = Dense(self.window_size)(enc_input)
        dense = Dense(self.window_size * 2)(dense)
        dropout = Dropout(dropout_amount)(dense)
        dense = Dense(self.window_size * 3)(dropout)
        dense = Dense(self.window_size * 2)(dense)
        dense = Dense(self.window_size)(dense)
        enc_out = Dense(compression)(dense)
        dec_input = Dense(compression)(dense)
        dense = Dense(self.window_size)(dec_input)
        dense = Dense(self.window_size * 2)(dense)
        dense = Dense(self.window_size * 3)(dense)
        dropout = Dropout(dropout_amount)(dense)
        dense = Dense(self.window_size * 2)(dropout)
        dec_out = Dense(self.window_size)(dense)

        self.enc_model = Model(inputs=[enc_input], outputs=[enc_out], name='Encoder Model')
        self.model = Model(inputs=[enc_input], outputs=[dec_out], name='Autoencoder Model')

    def build_cnn_model(self, compression, dropout_rate):
        enc_input = Input((self.window_size,))
        reshape = Reshape((1, self.window_size))(enc_input)
        cnn = Conv1D(self.window_size, 3, padding='same')(reshape)
        upscale = UpSampling1D()(cnn)
        cnn = Conv1D(self.window_size, 3, padding='same')(upscale)
        upscale = UpSampling1D()(cnn)
        cnn = Conv1D(self.window_size, 3, padding='same')(upscale)
        dropout = Dropout(dropout_rate)(cnn)
        pool = MaxPool1D()(dropout)
        cnn = Conv1D(self.window_size, 3, padding='same')(pool)
        pool = MaxPool1D()(cnn)
        enc_out = Conv1D(compression, 3, padding='same')(pool)
        dec_input = Conv1D(compression, 3, padding='same')(enc_out)
        upscale = UpSampling1D()(dec_input)
        cnn = Conv1D(self.window_size, 3, padding='same')(upscale)
        dropout = Dropout(dropout_rate)(cnn)
        upscale = UpSampling1D()(dropout)
        cnn = Conv1D(self.window_size, 3, padding='same')(upscale)
        pool = MaxPool1D()(cnn)
        cnn = Conv1D(self.window_size, 3, padding='same')(pool)
        pool = MaxPool1D()(cnn)
        dec_out = Conv1D(self.window_size, 3, padding='same')(pool)

        self.enc_model = Model(inputs=[enc_input], outputs=[enc_out], name='Encoder Model')
        self.model = Model(inputs=[enc_input], outputs=[dec_out], name='Autoencoder Model')

    def summary(self):
        print(self.model.summary())
        print(self.enc_model.summary())

    def plot_model(self):
        plot_model(self.enc_model, to_file="Encoder.png", show_shapes=True, show_layer_names=True)
        plot_model(self.model, to_file="Autoencoder.png", show_shapes=True, show_layer_names=True)
