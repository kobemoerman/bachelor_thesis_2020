import os
import operator

import pydicom as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.sparse import csc_matrix

def get_struct_file(path, file):
    """
    Get the ROI contour file from a given path.

    Inputs:
        path (str): directory path that contains the DICOM structure file
        file (str): DICOM structure folder name

    Return:
        struct_file (str): structure file
    """

    file = path + "/" + [f for f in os.listdir(path) if file  in f][0]

    struct_file = file + "/" + [st for st in os.listdir(file) if '.dcm' in st][0]

    return pd.dcmread(struct_file)

def get_roi_names(struct_data):
    """
    Return the names of different contour data

    Inputs:
        struct_data (dicom.dataset.FileDataset): contour dataset read by dicom.dcmread

    Return:
        roi_names (list): names of the contour
    """

    roi_names = [roi_seq.ROIName for roi_seq in list(struct_data.StructureSetROISequence)]

    return roi_names

def cfile2pixels(file, path, ROIContourSeq):
    """
    Given a contour file and path of related images, return the pixel array for contours and their corresponding images.

    Inputs:
        file (DICOM): filename of contour
        path (str): path that has image files
        ROIContourSeq (int): tells which sequence of contouring to use

    Return:
        contour_imgs (list): pairs of img_arr and contour_arr for a given contour file
    """

    # contour for the region of interest
    GTV = file.ROIContourSequence[ROIContourSeq]
    # get contour datasets in a list
    contours = [contour for contour in GTV.ContourSequence]
    contour_imgs = [coord2pixels(cdata, path) for cdata in contours]

    return contour_imgs

def coord2pixels(contour_dataset, path):
    """
    Given a contour and corresponding DICOM images, return 2d image and contour pixel data.

    Inputs:
        contour_dataset: the contour image sequence
        path (str): path to DICOM images

    Return:
        img_arr: 2d np.array of image with pixel intensities
        contour_arr: 2d np.array of contour with 0 and 1 labels
    """

    contour_coord = contour_dataset.ContourData
    # (x,y,z) coordinates of the contour in mm
    coord = []
    for i in range(0, len(contour_coord), 3):
        coord.append((contour_coord[i], contour_coord[i + 1], contour_coord[i + 2]))

    # extract the image id corresponding to the given contour
    img_ID = contour_dataset.ContourImageSequence[0].ReferencedSOPInstanceUID
    img = pd.read_file(find_image_UID(path,img_ID))
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

    return img_arr, contour_arr, img_ID

def find_image_UID(path, img_UID):
    """
    Find the DICOM image in the dataset with the corresponding SOP Instance UID

    Inputs:
        path (str): String that tells the path of all DICOM images
        img_UID (str): image Instance UID of the contour

    Return:
        img (str): path to read DICOM image
    """

    for s in os.listdir(path):
        img = path + '/' + s
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
    plt.imshow(masked_contour_arr, cmap='cool', interpolation='none', alpha=0.7)
    plt.show()
