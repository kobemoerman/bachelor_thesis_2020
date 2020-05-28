import os
import pickle
import operator

import numpy as np
import pydicom as pd

from progress.bar import Bar

os.chdir('..')
data_dir = os.getcwd() + "/database/Head-Neck-CT"

SEED = 12345

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

def crop_2d_image(_img, _cntr, _dim=80):
    """
    Crops a 2d array around the centre of the contour with specified dimensions.

    Inputs:
        _img (numpy.ndarray): floating point numpy array.
        _dim (int, int): required array shape. Default set to (180, 180).

    Return:
        (numpy.ndarray): floating point numpy array with _dim shape.
    """

    # find the location of the tumour
    row, col = np.where(_cntr)
    x, y = row[int(len(row)/2)], col[int(len(col)/2)]

    # set up the new dimensions
    startx = x - (_dim//2) + 1
    endx   = x + (_dim//2) + 1

    starty = y - (_dim//2) + 1
    endy   = y + (_dim//2) + 1

    # return the region of interest
    return _img[startx:endx, starty:endy], _cntr[startx:endx, starty:endy]

def fill_contour(_contour):
    """
    Transforms a 2d contour as to create a mask.

    Inputs:
        _contour (np.ndarray): list of pixel values.

    Return:
        (np.array): 2d contour mask.
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
            cntr_pixels[x].append((x,y))

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
            img  = np.array(temp[0])
            cntr = np.array(temp[1])

        # crop the CT image and contour data
        img, cntr = crop_2d_image(img, cntr)

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

def append_data(_folder, _parts, _processing):
    """
    Edit the data and assemble it together into a list.

    Inputs:
        _folder (list): list of patients to assemble.
        _parts (int): number of slices required per patient.
        _processing (str): data type that is being processed.

    Return:
        (list): list of images, contours, and labels.
    """
    data = []

    # create a progress bar
    bar  = Bar(_processing, max=len(_folder))

    for _file in _folder:
        # path to the patient directory
        path = data_dir+ '/' + _file
        # read the patient's label
        label = read_label(path)
        # read the patient's CT images
        img, cntr = read_data(path, _parts)
        # include to the data
        for _img, _cntr in zip(img, cntr):
            data.append((_img, label, _cntr))

        bar.next()

    bar.finish()

    return data


def distribute_data(_data):
    """
    Split the data equally with an established seed.

    Inputs:
        _data (list): list of images, contours, and labels.

    Return:
        (list, list): train and test sets.
    """
    # shuffle the data identically every time
    np.random.seed(SEED)
    np.random.shuffle(_data)

    # split 50/50
    split = int(len(_data) / 2)
    train = _data[:split]
    test  = _data[split:]

    return train, test


def load_data_MAASTRO(_parts=1):
    """
    Read the preprocessed data from the MAASTRO dataset.

    Inputs:
        _parts (int): number of slices to extract per patient.

    Return:
        (np.array, np.array): training and test sets.
    """
    # directories that are part of the MAASTRO study
    radiomic_dir = [f for f in os.listdir(data_dir) if 'radiomic' in f]

    print("\n--->\tLoading preprocessed CT images from the MAASTRO database")

    # read the preprocessed data
    data = append_data(radiomic_dir, _parts, 'Processing Train and Test')

    # split the data into training and testing sets
    train, test = distribute_data(data)

    return map(np.array, zip(*train)), map(np.array, zip(*test))


def load_data_MCGILL(_parts=1):
    """
    Read the preprocessed data from the MCGILL database.

    Inputs:
        _parts (int): number of slices to extract per patient.

    Return:
        (np.array, np.array): training and test sets.
    """
    # train and test directories that are part of the MCGILL study
    train_dir = [f for f in os.listdir(data_dir) if 'train' in f]
    test_dir  = [f for f in os.listdir(data_dir) if 'test' in f]

    print("\n--->\tLoading preprocessed CT images from the MCGILL database")

    # read the corresponding preprocessed data
    train = append_data(train_dir, _parts, 'Processing Train')
    test  = append_data(test_dir, _parts, 'Processing Test ')

    return map(np.array, zip(*train)), map(np.array, zip(*test))
