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
    # create new directory
    _dir = os.getcwd() + '/database/Model-Data/{}-slice'.format(_slices)
    Path(_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(_dir)

    # load data
    (x_train, x_label, x_contour) , (y_test, y_label, y_contour) = dp.load_data(_slices)

    print("Data shape:", np.array(x_train).shape)
    print("Label shape:", np.array(x_label).shape)
    print("Contour shape:", np.array(x_contour).shape)

    # create train files
    pickle.dump(np.array(x_train),
                open('train_data_{:02d}.pxl'.format(_slices), 'wb'))
    pickle.dump(np.array(x_label),
                open('train_label_{:02d}.pxl'.format(_slices), 'wb'))
    pickle.dump(np.array(x_contour),
                open('train_contour_{:02d}.pxl'.format(_slices), 'wb'))

    # create test files
    pickle.dump(np.array(y_test),
                open('test_data_{:02d}.pxl'.format(_slices), 'wb'))
    pickle.dump(np.array(y_label),
                open('test_label_{:02d}.pxl'.format(_slices), 'wb'))
    pickle.dump(np.array(y_contour),
                open('test_contour_{:02d}.pxl'.format(_slices), 'wb'))

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
