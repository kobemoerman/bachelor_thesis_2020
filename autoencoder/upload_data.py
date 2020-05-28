import os
import argparse
import pickle
import numpy as np
import data_prep as dp

from pathlib import Path

def upload_model_data(_slices):
    """
    Reads the preprocessed data and saves it in a new file.

    Inputs:
        _slices (int): number of slices to extract per patient.
    """
    # new directory path
    _dir = os.getcwd() + '/database/Model-Data/mask'

    """ load MCGILL data """
    (x_train, x_label, x_contour) , (y_test, y_label, y_contour) = dp.load_data_MCGILL(_slices)
    # check data shape
    print("Train shape:", np.array(x_train).shape)
    print("Test shape:", np.array(y_test).shape)
    print("Label shapes:", np.array(x_label).shape, np.array(y_label).shape)
    # create new directory
    path = _dir + '/MCGILL'
    Path(path).mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    # write data to directory
    write_file(x_train, x_label, x_contour, 'train')
    write_file(y_test, y_label, y_contour, 'test')

    """ load MAASTRO data """
    (x_train, x_label, x_contour) , (y_test, y_label, y_contour) = dp.load_data_MAASTRO(_slices)
    # check data shape
    print("Train shape:", np.array(x_train).shape)
    print("Test shape:", np.array(y_test).shape)
    print("Label shapes:", np.array(x_label).shape, np.array(y_label).shape)
    # create new directory
    path = _dir + '/MAASTRO'
    Path(path).mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    # write data to directory
    write_file(x_train, x_label, x_contour, 'train')
    write_file(y_test, y_label, y_contour, 'test')


def write_file(_data, _label, _contour, _type):
    """
    Write the data to the specified folder.

    Inputs:
        _data (np.array): list of pixel intensities.
        _label (np.array): list of labels.
        _contour (np.array): list of contour.
        _type (str): distinction between train and test data.
    """
    pickle.dump(np.array(_data), open(_type + '_data.pxl', 'wb'))
    pickle.dump(np.array(_label), open(_type + '_label.pxl', 'wb'))
    pickle.dump(np.array(_contour), open(_type + '_contour.pxl', 'wb'))

def main():
    """
    python3 upload_data.py -slices (int)

    Inputs:
        -slices (int): number of slices per patient.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-slices", type=int, required=True)
    args = parser.parse_args()

    upload_model_data(args.slices)

if __name__ == "__main__":
    main()
