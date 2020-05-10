import sys
import numpy as np
import matplotlib.pyplot as plt
import data_prep as ncia

from keras.datasets import mnist
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model

# size of the encoded representations
encoding_dim = 32

# size of input
img_size = 300**2

# input placeholder
input_img = Input(shape=(300, 300, 1))

x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

# autoencoder model
autoencoder = Model(input_img, decoded)

# use per-pixel binary crossentropy loss and Adadelta optimizer
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

# import the input data
(x_train, _, _), (x_test, _, _) = ncia.load_data()

# normalize the data
x_train = x_train.astype('float32') / 2000.
x_test  = x_test.astype('float32') / 2000.


# reshape the data
x_train = np.reshape(x_train, (len(x_train), 300, 300, 1))
x_test  = np.reshape(x_test, (len(x_test), 300, 300, 1))

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))

# encode and decode some digits (taken from test set)
decoded_imgs = autoencoder.predict(x_test)

n = 10  # how many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(300, 300))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + n)
    plt.imshow(decoded_imgs[i].reshape(300, 300))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

