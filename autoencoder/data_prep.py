import os
import sys
import pickle
import operator

import numpy as np
import pydicom as pd

sys.path.append('../data_preprocessing')
import utility

os.chdir('..')
data_dir = os.getcwd() + "/database/Head-Neck-CT"

def crop_2d_image(img, bounding=(300,300)):
    """
    """
    start  = tuple(map(lambda a, da: a//2-da//2, img.shape, bounding))
    end    = tuple(map(operator.add, start, bounding))
    slices = tuple(map(slice, start, end))

    return img[slices]

def read_data(_path, _parts):
    """
    """
    data   = os.listdir(_path)
    size   = len(data) - 1

    _parts = 2 if _parts * size < 10 else _parts + 1

    slices = [round(i * size / _parts) - 1 for i in range(1, _parts)]

    data_img, data_cntr = [], []
    for _file in slices:
        with open(_path + '/' + data[_file], 'rb') as f:
            temp = pickle.load(f)
            img  = temp[0]
            cntr = temp[1]

        # crop the CT image and contour data
        img, cntr = crop_2d_image(img), crop_2d_image(cntr)

        # clip the CT image to have values in the range [0,2000]
        np.clip(a=img, a_min=0, a_max=2000, out=img)

        data_img.append(img)
        data_cntr.append(cntr)

    return data_img, data_cntr

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
    for (_img, _label, _cntr) in _data:
        (l0, l1)[_label == 1].append((_data, _label, _cntr))

    np.random.shuffle(l0)
    np.random.shuffle(l1)

    train, test = split_data(l0,l1)

    np.random.shuffle(train)
    np.random.shuffle(test)

    return train, test

def ncia_read_data(_parts=1):
    """
    """
    data = []

    print("---\tREADING DATA\t---")
    for _file in os.listdir(data_dir):
        path  = data_dir + '/' + _file
        label = read_label(path)
        img, cntr = read_data(path, _parts)

        for _img, _cntr in zip(img, cntr):
            data.append((_img, label, _cntr))

    print("---\tDISTRIBUTING DATA\t---")
    train, test = distribute_data(data)

    return map(list, zip(*train)), map(list, zip(*test))


def main():
    """
    """
    (train_data, train_labels, _), (test_data, test_labels, _) = ncia_read_data()

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
