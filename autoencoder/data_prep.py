import os
import sys
import pickle
import operator

import numpy as np
import pydicom as pd

sys.path.append('../data_preprocessing')
import utility as util

os.chdir('..')
data_dir = os.getcwd() + "/database/Head-Neck-CT"

def _dict(default_type):
    """
    Dictionary.
    """
    class Dictionary(dict):
        def __getitem__(self, key):
            if key not in self:
                dict.__setitem__(self, key, default_type())
            return dict.__getitem__(self, key)
    return Dictionary()

def crop_2d_image(_img, _dim=(300,300)):
    """
    Crops a 2d array around its centre to specified dimensions.

    Inputs:
        _img (numpy.ndarray): floating point numpy array.
        _dim (int, int): required array shape. Default set to (300, 300).

    Return:
        (numpy.ndarray): floating point numpy array with _dim shape.
    """
    start  = tuple(map(lambda a, da: a//2-da//2, _img.shape, _dim))
    end    = tuple(map(operator.add, start, _dim))
    slices = tuple(map(slice, start, end))

    return _img[slices]

def fill_contour(_contour):
    """
    Transforms a 2d contour as to create a mask

    Inputs:
        _contour (np.ndarray): list of pixel values.

    Return:
        (np.array): 2d contour mask
    """
    # left to right
    row, col = np.where(_contour)
    row, col = contour_mask(_contour, row, col)
    _contour[row, col] = 1

    # top to bottom
    row, col = np.where(_contour)
    col, row = contour_mask(_contour, col, row)
    _contour[row, col] = 1

    return _contour

def contour_mask(_contour, _row, _col):
    """
    Transforms the contour rows as to create a mask.

    Inputs:
        _contour (np.ndarray): list of pixel values.
        _row (np.ndarray): row indices of the contour.
        _col (np.ndarray): column indices of the contour.
    Return:
        (zip): row and column indices to fill in.
    """
    cntr_pixels = _dict(list)

    # initialise dictionary
    for x, y in zip(_row, _col):
        cntr_pixels[x].append((x,y))

    cntr_mask = []
    for x in cntr_pixels:
        # find the leftmost and rightmost pixels for the current row
        temp = cntr_pixels[x]
        _min = min(temp, key = lambda t: t[1])[1]
        _max = max(temp, key = lambda t: t[1])[1]

        # fill the pixels between _min and _max
        for y in range(_min, _max):
            if (x,y) not in temp: cntr_pixels[x].append((x,y))

        cntr_mask.append(cntr_pixels[x])

    # transform to a list of tuples
    cntr_mask = list(set([pixel for area in cntr_mask for pixel in area]))

    return zip(*cntr_mask)

def read_data(_path, _parts):
    """
    Read n slices from a patient corresponding to the CT scan's pixel intensities and tumour delineation.

    Inputs:
        _path (str): path to the required data.
        _parts (int): number of slices required.

    Return:
        (list, list) pixel intensities and tumour delineations
    """
    data   = os.listdir(_path)
    size   = len(data) - 1

    # only retrieve one slice if the gross tumour volume is too small
    _parts = 2 if _parts * size < 10 else _parts + 1

    # equally spaced index of the n slices
    slices = [round(i * size / _parts) - 1 for i in range(1, _parts)]

    data_img, data_cntr = [], []
    for _file in slices:
        # read the data
        with open(_path + '/' + data[_file], 'rb') as f:
            temp = pickle.load(f)
            img  = temp[0]
            cntr = temp[1]

        # crop the CT image and contour data
        img, cntr = crop_2d_image(img), crop_2d_image(cntr)

        # create a mask for the contour
        cntr = fill_contour(cntr)

        # clip the CT image to have values in the range [0,2000]
        np.clip(a=img, a_min=0, a_max=2000, out=img)

        data_img.append(img)
        data_cntr.append(cntr)

    return data_img, data_cntr

def read_label(_path):
    """
    Read the patient's metastasis label.

    Inputs:
        _path (str): path to the required data.

    Return:
        (int): corresponding patient's label.
    """
    with open(_path + '/metastasis.pxl', 'rb') as f:
        value = pickle.load(f)

    return value

def split_data(_x, _y):
    """
    Swap half the values of one list with another list.

    Inputs:
        _x (list): vector of floating points.
        _y (list): vector of floating poitns.

    Return:
        (list, list): interchanged lists.
    """
    half_x, half_y = len(_x)//2, len(_y)//2

    dx = _x[half_x:] + _y[half_y:]
    dy = _x[:half_x] + _y[:half_y]

    np.random.shuffle(dx)
    np.random.shuffle(dy)

    return dx, dy

def distribute_data(_data):
    """
    Equally distribute the data between training and test sets.

    Inputs:
        _data (numpy.ndarray): list of pixel intensities, contours, labels.

    Return:
        (list): training and test sets.
    """
    l0, l1 = [], []

    # separate data according to their label
    for (_img, _label, _cntr) in _data:
        (l0, l1)[_label == 1].append((_data, _label, _cntr))

    # distribute labels equally amongst train and test
    train, test = split_data(l0,l1)

    return train, test

def ncia_read_data(_parts=1):
    """
    Read the preprocessed data from the NCIA database.

    Inputs:
        _parts (int): number of slices to extract per patient.

    Return:
        (list): training and test sets.
    """
    data = []

    print("--->\tdistributing data")

    # read data
    for _file in os.listdir(data_dir):
        path  = data_dir + '/' + _file
        label = read_label(path)
        img, cntr = read_data(path, _parts)

        for _img, _cntr in zip(img, cntr):
            data.append((_img, label, _cntr))

    # distribute data
    train, test = distribute_data(data)

    print("--->\tdone")

    return map(list, zip(*train)), map(list, zip(*test))

ncia_read_data(1)
