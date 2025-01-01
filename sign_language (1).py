# -*- coding: utf-8 -*-
"""sign_language.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MTzy3r2N08-oBDDURWU6JI6Vn-WAtRtu

uni: nll2128 Nancy Liddle

# MNIST Sign Language
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.src.layers.activations import activation

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import keras
import tensorflow
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

class SignLanguage:
    def __init__(self):
        self.model = None
        self.num_classes = None
        self.data = {
            "train": None,
            "test" : None
        }
        self.create_model()

    def create_model(self):
        """
        Create a CNN model and save it to self.model
        """
        # TODO: Create a Sequential model
        #tensorflow.keras.Input(shape=(28, 28, 1))
        model = Sequential([
            tensorflow.keras.Input(shape=(28, 28, 1)),
            Conv2D(32, (5, 5), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),

            Conv2D(16, (5, 5), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),

            Flatten(),
            Dense(units=512, activation='relu'),
            Dropout(0.25),
            Dense(25, activation='softmax')
        ])

        # TODO: Compile the model with categorical_crossentropy
        model.compile('adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])


        self.model = model

    def prepare_data(self, images, labels):
        """
        Use this method to normalize the dataset and split it into train/test.
        Save your data in self.data["train"] and self.data["test"] as a tuple
        of (images, labels)

        :param images numpy array of size (num_examples, 28*28)
        :param labels numpy array of size (num_examples, )
        """
        # TODO : split into training and validation set
        # TODO : reshape each example into a 2D image (28, 28, 1)
        images = images/255.0
        images = images.reshape(-1,28,28,1)

        self.num_classes = labels.max()+1  # Automatically detect the number of classes
        labels = to_categorical(labels, self.num_classes)

        x_train, x_test, y_train, y_test=train_test_split(images, labels, test_size=0.2, random_state=42)
        self.data = {
            "train": (x_train, y_train),
            "test" : (x_test, y_test)
        }
    def train(self, batch_size:int=128, epochs:int=50, verbose:int=1):
        """
        Use model.fit() to train your model. Make sure to return the history for a neat visualization.

        :param batch_size The batch size to use for training
        :param epochs     Number of epochs to use for training
        :param verbose    Whether or not to print training output
        """
        history = self.model.fit(self.data["train"][0], self.data["train"][1], epochs=epochs, batch_size=batch_size, verbose=verbose, validation_data=self.data["test"])
        return history

    def predict(self, data):
        """
        Use the trained model to predict labels for test data.

        :param data: numpy array of test images
        :return a numpy array of test labels. array size = (num_examples, )
        """

        # Don't forget to normalize the data in the same way as training data
        # self.model.predict() and np.argmax( , axis=1) might help
        data = data/255.0
        data = data.reshape(-1,28,28,1)
        predictions = self.model.predict(data)

        return np.argmax(predictions, axis=1).tolist()

    def visualize_data(self, data):
        """
        Visualizing the hand gestures

        :param data: numpy array of images
        """
        if data is None: return

        nrows, ncols = 5, 5
        fig, axs = plt.subplots(nrows, ncols, figsize=(10, 10), sharex=True, sharey=True)
        plt.subplots_adjust(wspace=0, hspace=0)

        for i in range(nrows):
            for j in range(ncols):
                axs[i][j].imshow(data[0][i*ncols+j].reshape(28, 28), cmap='gray')

        plt.show()

    def visualize_accuracy(self, history):
        """
        Plots out the accuracy measures given a keras history object

        :param history: return value from model.fit()
        """
        if history is None: return

        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title("Accuracy")
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend(['train','test'])
        plt.show()

"""# Grading Script

Do NOT modify this section
"""

if __name__=="__main__":
    train = pd.read_csv('/content/test.csv')
    test  = pd.read_csv('/content/train.csv')

    train_labels, test_labels = train['label'].values, test['label'].values
    train.drop('label', axis=1, inplace=True)
    test.drop('label', axis=1, inplace=True)

    num_classes = test_labels.max() + 1
    train_images, test_images = train.values, test.values

    print(train_images.shape, train_labels.shape, test_images.shape, test_labels.shape)



if __name__=="__main__":
    my_model = SignLanguage()
    my_model.prepare_data(train_images, train_labels)

if __name__=="__main__":
    my_model.visualize_data(my_model.data["train"])

if __name__=="__main__":
    history = my_model.train(epochs=30, verbose=1)
    my_model.visualize_accuracy(history)

if __name__=="__main__":
    y_pred = my_model.predict(test_images)
    accuracy = accuracy_score(test_labels, y_pred)
    print(accuracy)