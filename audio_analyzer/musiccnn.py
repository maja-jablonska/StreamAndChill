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

def load_train_valid_data(path: str) -> Tuple[np.array, np.array, np.array, np.array]:
  y_train_final = np.load(join(path, _Y_TRAIN))
  y_valid_final = np.load(join(path, _Y_VALID))
  x_train = np.load(join(path, _X_TRAIN))
  x_valid = np.load(join(path, _X_VALID))

  return TrainData(x_train, y_train_final, x_valid, y_valid_final)


def musicccnn(n_classes, input_shape) -> tfk.Model:
  model = tf.keras.Sequential()

  model.add(tf.keras.layers.Conv2D(24 , (5 , 5) , strides=(1 , 1) , input_shape=input_shape))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.MaxPooling2D((4,2) , strides=(4 , 2)))
  model.add(tf.keras.layers.Activation('relu'))

  model.add(tf.keras.layers.Conv2D(48 , (5 , 5) , padding='valid'))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.MaxPooling2D((4 , 2) , strides=(4 , 2)))
  model.add(tf.keras.layers.Activation('relu'))

  model.add(tf.keras.layers.Conv2D(48 , (5 , 5) , padding='valid'))
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
  return tfk.models.load_model(ckpt_path)

def train_get_model(data_path: str) -> tfk.Model:
  data = load_train_valid_data(data_path)
  model = musicccnn(n_classes=2, input_shape= (128, 128, 1))

  callbacks = [
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.1, patience=10, min_lr=0.00001, verbose=1),
  ]

  model.compile(
      optimizer='Adam',
      loss='categorical_crossentropy',
      metrics = ['accuracy']
  )

  model.fit(
      x=data.x_train,
      y=data.y_train,
      epochs=200,
      batch_size=64,
      validation_data=(data.x_valid , data.y_valid),
      callbacks=callbacks,
  )

  return model

def create_spectrogram(track_path):
  y, sr = librosa.load(track_path, duration=2.97)
  spect = librosa.feature.melspectrogram(y=y, sr=sr)
  return spect

def prepare_infer_from_sample(path: str):
  X = np.empty((0 , 128 , 128))
  spect = create_spectrogram(path)
  X = np.append(X, [spect], axis=0)
  X = np.array([x.reshape((128 , 128 , 1)) for x in X])
  return X

def check_if_aggressive(model: tfk.Model, mp3_path: str) -> bool:
  infer = model(prepare_infer_from_sample(mp3_path))
  return infer[1] >= 0.9