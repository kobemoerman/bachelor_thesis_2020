import numpy as np

import matplotlib.pyplot as plt

from keras.datasets import mnist
from keras.layers import Input, Dense
from keras.models import Model

# size of the encoded representations
encoding_dim = 32

# size of input
img_size = 28**2

# input placeholder
input_img = Input(shape=(img_size,))
# encoded representation of the input
encoded = Dense(encoding_dim, activation='relu')(input_img)
# lossy reconstruction of the input
decoded = Dense(img_size, activation='sigmoid')(encoded)

# autoencoder model
autoencoder = Model(input_img, decoded)

# encoder model
encoder = Model(input_img, encoded)

# decoder model
encoded_input = Input(shape=(encoding_dim,))
decoded_layer = autoencoder.layers[-1]
decoder = Model(encoded_input, decoded_layer(encoded_input))

# use per-pixel binary crossentropy loss and Adadelta optimizer
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

# import the input data
(x_train, _), (x_test, _) = mnist.load_data()

# normalize the data
x_train = x_train.astype('float32') / 255.
x_test  = x_test.astype('float32') / 255.

# reshape the data
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test  = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

print(x_train.shape)
print(x_test.shape)

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))

# encode and decode some digits (taken from test set)
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

n = 10  # how many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
