import os
import re
import sys
import pickle
import operator
import numpy as np
import pydicom as pd

import clinic as data

from pathlib import Path

os.chdir('..')
save_dir = os.getcwd() + "/database/Head-Neck-CT"

# list of directory names that contain CT images
dict_CT = ['^\d*.000000-standardfull-\d*$',
           '^\d*.000000-ct images-\d*$',
           '^\d*.000000-ctnormal\w*-\d*$',
           '^\d*.000000-merged-\d*$',
           '^\d*.000000-ct std-\d*$']

# RTstruct directory containing the structure file
struct_ROI   = '^\d*.000000-RTstructCTsim-CTPET-CT-\d*$'
# pinnacle directory containing the structure file
pinnacle_ROI = 'Pinnacle (ROI|POI)-\d*$'

def get_MAASTRO_CT_directory(_path):
    """
    Get the path to the CT images directory for a given patient from MAASTRO clinic.

    Inputs:
        _path (str): path to patient directory.

    Return:
        (str): path to directory with CT images.
    """
    # directories with CT or PET images
    dir_CT = [_folder for _folder in os.listdir(_path) if _folder.isdigit()]

    for _folder in dir_CT:
        _temp = _path + '/' + _folder + '/'
        # read first DIOCM file
        _file = pd.dcmread(_temp + os.listdir(_temp)[0])
        # save the folder for CT images
        if _file.Modality == 'CT': path_CT = _folder

    try:
        return _path + '/' + path_CT
    except:
        return "ERROR CT: No directory found."

def get_MCGILL_CT_data(_path):
    """
    Get the path to the CT images directory for a given patient from McGill clinic.

    Inputs:
        _path (str): path to patient directory.

    Return:
        (str): path to directory with CT images.
    """

    # find the directory with the CT images
    for path, directories, files in os.walk(_path):
        # save the folder that contains any key word from the given dictionary
        for _dir in directories:
            for regex in dict_CT:
                if re.match(regex, _dir, re.IGNORECASE):
                    return path + '/' + _dir

    return "ERROR CT: No directory found."

def get_ROI_index(_list, _item):
    """
    Get the index of the ROI corresponding to the GTV.

    Inputs:
        _list (list): all ROI applicable to the CT images.
        _item (str): name of the ROI for the primary tumor volume.

    Return:
        (int): GTV index or index containg 'GTV' as substring.
    """
    try:
        return operator.indexOf(_list, _item)
    except:
        return operator.indexOf(_list, [ROI for ROI in _list if 'GTV' in ROI][0])

def get_MCGILL_ROI_data(_path):
    """
    Get the structure file from the patient directory.

    Inputs:
        _path (str): current path to the patient directory.

    Return:
        (str, str) path to the required directory with the file name
    """

    for path, directories, files in os.walk(_path):
        for _dir in directories:
            if re.match(struct_ROI, _dir):
                return path, _dir
            if re.match(pinnacle_ROI, _dir):
                struct_path = path
                struct_dir  = _dir

    try:
        return struct_path, struct_dir
    except:
        return "ERROR ROI: No directory found.", "ERROR type."


def get_MAASTRO_CT_ROI_data(_path):
    """
    Get the CT images and structure file from the patient directory.

    Inputs:
        _path (str): current path to the patient directory.

    Return:
        (str, str): path to the required data and structure file.
    """
    regex = '^\d.000000-'

    path_CT  = _path + '/' + os.listdir(_path)[0]
    type_ROI = [i for i in os.listdir(path_CT) if re.match(regex,i)][0]

    # return the CT and ROI paths
    try:
        return path_CT, type_ROI
    except:
        return "ERROR CT: No directory found.", "ERROR type."


def write_file_ROI(_list_CT, _recc, _prefix, _idx):
    """
    Write the pixel intensities for each patient to a new directory.

    Inputs:
        _list_CT (list): contains the pixel intensities for the CT image and corresponding contour.
        _recc (int): true if there is locoregional/distant metastasis or death, else false.
        _prefix (str): folder name to save patient data.
        _idx (int): new unique patient reference.
    """
    # create new directory
    _sub = save_dir + _prefix.format(_idx)
    Path(_sub).mkdir(parents=True, exist_ok=True)
    os.chdir(_sub)

    # save metastasis value
    with open('metastasis.pxl', 'wb') as f:
        pickle.dump(_recc, f)

    # save pixel intensities and their respective contour for every slice
    for idx, image in enumerate(_list_CT):
        CT_image, CT_contour = image
        with open('{:03d}.pxl'.format(idx+1), 'wb') as f:
            pickle.dump(np.array([CT_image, CT_contour]), f)


