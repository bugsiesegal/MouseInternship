from keras import Model
from keras.layers import *
from keras.utils.vis_utils import plot_model
from keras.optimizers import *
import Utils
import matplotlib.pyplot as plt


class FiberPhotometryModel:
    enc_model: Model
    model: Model

    def __init__(self, window_size, learning_rate):
        self.enc_model = None
        self.model = None
        self.window_size = window_size
        self.lr = learning_rate
        self.optimizer = Adam(learning_rate)

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

        self.enc_model = Model(inputs=[enc_input], outputs=[enc_out], name='Encoder_Model')
        self.model = Model(inputs=[enc_input], outputs=[dec_out], name='Autoencoder_Model')

        self.enc_model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])
        self.model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])

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
        cnn = Conv1D(self.window_size, 3, padding='same')(pool)
        dec_out = Reshape((self.window_size,))(cnn)

        self.enc_model = Model(inputs=[enc_input], outputs=[enc_out], name='Encoder_Model')
        self.model = Model(inputs=[enc_input], outputs=[dec_out], name='Autoencoder_Model')

        self.enc_model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])
        self.model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])

    def summary(self):
        print(self.model.summary())
        print(self.enc_model.summary())

    def plot_model(self):
        plot_model(self.enc_model, to_file="Encoder.png", show_shapes=True, show_layer_names=True)
        plot_model(self.model, to_file="Autoencoder.png", show_shapes=True, show_layer_names=True)

    def train(self, data: list[Utils.Windows], epochs=1, history_plot=True):
        history_accuracy = []
        history_accuracy_val = []
        for windows in data:
            if windows.data.any(None):
                history = self.model.fit(windows.data, windows.data, epochs=epochs, validation_split=0.2)
                history_accuracy += history.history['accuracy']
                history_accuracy_val += history.history['val_accuracy']

        if history_plot:
            plt.plot(history_accuracy)
            plt.plot(history_accuracy_val)
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()

    def predict(self, data):
        return self.model.predict(data)