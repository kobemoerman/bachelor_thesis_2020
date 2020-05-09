import os
import operator

import pydicom as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.sparse import csc_matrix

def get_struct_file(_path, _file):
    """
    Get the ROI contour file from a given path.

    Inputs:
        _path (str): directory path that contains the DICOM structure file.
        _file (str): DICOM structure folder name.

    Return:
        struct_file (dicom): structure file.
    """

    file = _path + '/' + [f for f in os.listdir(_path) if _file in f][0]

    struct_file = file + '/' + [st for st in os.listdir(file) if '.dcm' in st][0]

    return pd.dcmread(struct_file)

def get_roi_names(_data):
    """
    Return the names of different contour data.

    Inputs:
        _data (dicom.dataset.FileDataset): contour dataset read by dicom.dcmread.

    Return:
        roi_names (list): names of the contour.
    """

    roi_names = [roi_seq.ROIName for roi_seq in list(_data.StructureSetROISequence)]

    return roi_names

def contour_to_pixel(_file, _path, _seq):
    """
    Given a contour file and path of related images, return the pixel array for contours and their corresponding images.

    Inputs:
        _file (dicom): file with contour structure.
        _path (str): path that has CT images.
        _seq (int): tells which sequence of contouring to use.

    Return:
        contour_imgs (list): pairs of img_arr and contour_arr for a given contour file
    """

    # contour for the region of interest
    GTV = _file.ROIContourSequence[_seq]
    # get contour datasets in a list
    contours = [contour for contour in GTV.ContourSequence]
    contour_imgs = [coord_to_pixel(cdata, _path) for cdata in contours]

    return contour_imgs

def coord_to_pixel(_contour, _path):
    """
    Given a contour and corresponding DICOM images, return 2d image and contour pixel data.

    Inputs:
        _contour: the contour image sequence
        _path (str): path to DICOM images

    Return:
        img_arr: 2d np.array of image with pixel intensities
        contour_arr: 2d np.array of contour with 0 and 1 labels
    """

    contour_coord = _contour.ContourData
    # (x,y,z) coordinates of the contour in mm
    coord = []
    for i in range(0, len(contour_coord), 3):
        coord.append((contour_coord[i], contour_coord[i + 1], contour_coord[i + 2]))

    # extract the image id corresponding to the given contour
    img_ID = _contour.ContourImageSequence[0].ReferencedSOPInstanceUID
    img = pd.read_file(find_image_UID(_path, img_ID))
    img_arr = img.pixel_array

    # physical distance between the center of each pixel
    x_spacing, y_spacing = float(img.PixelSpacing[0]), float(img.PixelSpacing[1])

    # this is the center of the upper left voxel
    origin_x, origin_y, _ = img.ImagePositionPatient

    # it is mapped as y, x
    pixel_coords = [(np.ceil((y - origin_y) / y_spacing), np.ceil((x - origin_x) / x_spacing)) for x, y, _ in coord]

    # get contour data for the image
    rows = []
    cols = []
    for i, j in list(set(pixel_coords)):
        rows.append(i)
        cols.append(j)

    contour_arr = csc_matrix((np.ones_like(rows), (rows, cols)), dtype=np.int8, shape=(img_arr.shape[0], img_arr.shape[1])).toarray()

    return img_arr, contour_arr

def find_image_UID(_path, img_UID):
    """
    Find the DICOM image in the dataset with the corresponding SOP Instance UID

    Inputs:
        _path (str): String that tells the path of all DICOM images
        img_UID (str): image Instance UID of the contour

    Return:
        img (str): path to read DICOM image
    """

    for s in os.listdir(_path):
        img = _path + '/' + s
        f = pd.read_file(img)
        if f.SOPInstanceUID == img_UID: return img

def plot_2d_contour(img_arr, contour_arr, figsize=(20,20)):
    """
    Shows 2d CT image with contour

    Inputs:
        img_arr: 2d np.array image array with pixel intensities
        contour_arr: 2d np.array contour array with pixels of 1 and 0
    """

    masked_contour_arr = np.ma.masked_where(contour_arr == 0, contour_arr)
    plt.figure(figsize=figsize)
    plt.subplot(1,2,1)
    plt.imshow(img_arr, cmap='gray', interpolation='none')
    plt.subplot(1,2,2)
    plt.imshow(img_arr, cmap='gray', interpolation='none')
    plt.imshow(masked_contour_arr, cmap='autumn', interpolation='none', alpha=0.7)
    plt.show()
