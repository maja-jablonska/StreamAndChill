import numpy as np
from typing import Tuple
import librosa
import tensorflow as tf
import tensorflow.keras as tfk
import tensorflow.keras.layers as l
from dataclasses import dataclass
from os.path import join


@dataclass
class TrainData:
    x_train: np.array
    y_train: np.array
    x_valid: np.array
    y_valid: np.array


_X_TRAIN = 'X_train.npy'
_Y_TRAIN = 'y_train_final.npy'
_X_VALID = 'X_valid.npy'
_Y_VALID = 'y_valid_final.npy'


def load_train_valid_data(path: str) -> TrainData:
    """Loads train and valid data and put that into dataclass

    Args:
        path (str): path to a folder where data is stored

    Returns:
      TrainData: train data stored in dataclass
    """
    y_train_final = np.load(join(path, _Y_TRAIN))
    y_valid_final = np.load(join(path, _Y_VALID))
    x_train = np.load(join(path, _X_TRAIN))
    x_valid = np.load(join(path, _X_VALID))

    return TrainData(x_train, y_train_final, x_valid, y_valid_final)


def musicccnn(n_classes: int, input_shape: Tuple[int]) -> tfk.Model:
    """Creates CNN Network for the music analysis.
       Input of the networks is a batched tensor of shape (bs, 128, 128, 1)
       which represents spectrogram. The output is single tensor of shape (bs, 2)
       representing probability of being calm ([0]) or being aggressive music ([1]).

    Args:
        n_classes (int): number of classes which classifier recognizes
        input_shape (Tuple[int]): input shape

    Returns:
        tfk.Model: model for recognizing music mood
    """
    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Conv2D(
        24, (5, 5), strides=(1, 1), input_shape=input_shape))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((4, 2), strides=(4, 2)))
    model.add(tf.keras.layers.Activation('relu'))

    model.add(tf.keras.layers.Conv2D(48, (5, 5), padding='valid'))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((4, 2), strides=(4, 2)))
    model.add(tf.keras.layers.Activation('relu'))

    model.add(tf.keras.layers.Conv2D(48, (5, 5), padding='valid'))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Activation('relu'))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(64))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(n_classes))
    model.add(tf.keras.layers.Activation('softmax'))

    return model


def load_ckpt_model(ckpt_path: str) -> tfk.Model:
    """loads checkpoint and returns a model

    Args:
        ckpt_path (str): path to the checkpoint

    Returns:
        tfk.Model: TF2 Model
    """
    return tfk.models.load_model(ckpt_path)


def train_get_model(data_path: str) -> tfk.Model:
    """Trains and return trained model

    Args:
        data_path (str): path to the train, valid data

    Returns:
        tfk.Model: TF2 Model
    """
    data = load_train_valid_data(data_path)
    model = musicccnn(n_classes=2, input_shape=(128, 128, 1))

    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(
            factor=0.1, patience=10, min_lr=0.00001, verbose=1),
    ]

    model.compile(
        optimizer='Adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(
        x=data.x_train,
        y=data.y_train,
        epochs=200,
        batch_size=64,
        validation_data=(data.x_valid, data.y_valid),
        callbacks=callbacks,
    )

    return model


def create_spectrogram(track_path: str) -> Tuple:
    """Creates spectrogram of the track

    Args:
        track_path (str): path to the music track

    Returns:
        Tuple: track spectrogram
    """
    y, sr = librosa.load(track_path, duration=2.97)
    spect = librosa.feature.melspectrogram(y=y, sr=sr)
    return spect


def prepare_infer_from_sample(path: str) -> np.array:
    """Prepares batch for the model inference

    Args:
        path (str): path to the sound track

    Returns:
        np.array: batch ready for the inference
    """
    X = np.empty((0, 128, 128))
    spect = create_spectrogram(path)
    X = np.append(X, [spect], axis=0)
    X = np.array([x.reshape((128, 128, 1)) for x in X])
    return X


def check_if_aggressive(model: tfk.Model, mp3_path: str) -> bool:
    """Checks if sound isn't calm 

    Args:
        model (tfk.Model): TF2 Model - binary classifier
        mp3_path (str): path to the track

    Returns:
        bool: true if track seems to be aggressive, false otherwise
    """
    infer = model(prepare_infer_from_sample(mp3_path))
    probability = infer[0][1]
    trashhold = 0.9
    return probability >= trashhold
