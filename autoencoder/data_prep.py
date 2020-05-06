import os
import sys
import pickle
import operator

import numpy as np
import pydicom as pd

os.chdir('..')
data_dir = os.getcwd() + "/database/Head-Neck-CT"

def crop_2d_image(img, bounding=(300,300)):
    """
    """
    start  = tuple(map(lambda a, da: a//2-da//2, img.shape, bounding))
    end    = tuple(map(operator.add, start, bounding))
    slices = tuple(map(slice, start, end))

    return img[slices]

def read_data(_path):
    """
    """
    data = os.listdir(_path)
    img_slice = str(round(len(data)/2))

    with open(_path + '/' + img_slice + '.pxl', 'rb') as f:
        temp = pickle.load(f)
        img  = temp[0]
        cntr = temp[1]

    # crop the CT image and contour data
    img, cntr = crop_2d_image(img), crop_2d_image(cntr)

    # clip the CT image to have values in the range [0,2000]
    np.clip(a=img, a_min=0, a_max=2000, out=img)

    return img, cntr

def read_label(_path):
    """
    """
    with open(_path + '/metastasis.pxl', 'rb') as f:
        value = pickle.load(f)

    return value

def split_data(_x, _y):
    """
    """
    half_x, half_y = len(_x)//2, len(_y)//2

    dx = _x[half_x:] + _y[half_y:]
    dy = _x[:half_x] + _y[:half_y]

    return dx, dy

def distribute_data(_data):
    """
    """
    l0, l1 = [], []
    for (_data, _label) in _data:
        (l0, l1)[_label == 1].append((_data, _label))

    np.random.shuffle(l0)
    np.random.shuffle(l1)

    train, test = split_data(l0,l1)

    np.random.shuffle(train)
    np.random.shuffle(test)

    return train, test

def main():
    """
    """
    _data = []

    print("--- READING DATA ---")
    for _file in os.listdir(data_dir):
        path = data_dir + '/' + _file
        data, _ = read_data(path)
        label   = read_label(path)
        _data.append((data, label))

    print("--- DISTRIBUTING DATA ---")
    train, test = distribute_data(_data)

if __name__ == "__main__":
    main()

"""
# normalize array
img_final = img_resampled/2000

# overlap contour array to normalized image array
test = np.array(np.zeros((350,350)),dtype=np.uint8)
idx  = np.where(contour_resampled == 1)
img_contour = img_final
img_contour[idx[0], idx[1]] = 1
"""
