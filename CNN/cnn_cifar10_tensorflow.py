# -*- coding: utf-8 -*-
"""CNN-Cifar10-Tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PiR5-XTcKeJdDZ3Xa_29OpylSUiyi-Ey
"""

import tensorflow as tf
from tensorflow.keras import datasets,layers,models,regularizers
import matplotlib.pyplot as plt

(train_images,train_labels),(test_images,test_labels) = datasets.cifar10.load_data()

# image normalization
train_images,test_images = train_images/255.0,test_images/255.0

"""# verify data with visualization"""

class_names = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']

plt.figure(figsize=(10,10))
for i in range(25):
  plt.subplot(5,5,i+1)
  # set ticks 刻度
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(train_images[i],cmap=plt.cm.binary)

  plt.xlabel(class_names[train_labels[i][0]])
plt.show()

"""# define Simple Model"""

model = models.Sequential()
model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3),activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3),activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64,activation='relu'))
# output 10 classes
model.add(layers.Dense(10))

"""# check model"""

model.summary()

"""# train model"""

model.compile(optimizer='adam',loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])
history = model.fit(train_images,train_labels,epochs=10,validation_data=(test_images,test_labels))

"""# model evaluation"""

# accuracy: acc of train data (number of predictions matching labels/total count)
# val_accuracy: acc of test data
plt.plot(history.history['accuracy'],label='accuracy')
plt.plot(history.history['val_accuracy'],label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5,1])
plt.legend(loc='lower right')
plt.show()