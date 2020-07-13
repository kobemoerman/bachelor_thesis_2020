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
    _dir = os.getcwd() + '/database/Model-Data/128'

    """ load MCGILL data """
    # x=data, y=label, c=clinical, z=contour
    (train_x, train_y, train_c, train_z), (test_x, test_y, test_c, test_z) = dp.load_data_MCGILL(_slices)
    # check data shape
    print("Train shape:", np.array(train_x).shape)
    print("Test shape:", np.array(test_x).shape)
    print("Label shapes:", np.array(train_y).shape, np.array(test_y).shape)
    # create new directory
    path = _dir + '/MCGILL'
    Path(path).mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    # write data to directory
    write_file(train_x, train_y, train_c, train_z, 'train')
    write_file(test_x, test_y, test_c, test_z, 'test')

    """ load MAASTRO data """
    # x=data, y=label, c=clinical, z=contour
    (train_x, train_y, train_c, train_z), (test_x, test_y, test_c, test_z) = dp.load_data_MAASTRO(_slices)
    # check data shape
    print("Train shape:", np.array(train_x).shape)
    print("Test shape:", np.array(test_x).shape)
    print("Label shapes:", np.array(train_y).shape, np.array(test_y).shape)
    # create new directory
    path = _dir + '/MAASTRO'
    Path(path).mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    # write data to directory
    write_file(train_x, train_y, train_c, train_z, 'train')
    write_file(test_x, test_y, test_c, test_z, 'test')

def write_file(_data, _label, _clinical, _contour, _type):
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
    pickle.dump(np.array(_clinical), open(_type + '_clinical.pxl', 'wb'))
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
