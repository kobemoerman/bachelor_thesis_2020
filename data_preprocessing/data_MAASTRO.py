import os
import csv
import argparse

import utility as util
import read_data as rd

# event distant metastasis (Y)
d_col = 24
# event local recurrence (U)
l_col = 20
# event overall survival (Q)
s_col = 16

home_dir = os.getcwd() + "/database/HEAD-NECK-RADIOMICS-HN1"
info_csv = os.getcwd() + "/database/HEAD-NECK-RADIOMICS-HN1 Clinical data.csv"

def get_data_clinic(write):
    """
    Retrive the ROI and corresponding CT images. Write the pixel intensities to a new directory.

    Inputs:
        write (bool): determine whether to write pixel intensities to new directory
   """

    with open(info_csv, newline='') as f:
        next(f)
        _info = list(csv.reader(f))

    for idx, _folder in enumerate(os.listdir(home_dir)):
        print("Processing patient " + _folder)
        _path = home_dir + '/' + _folder

        # path to the ROI and CT files
        patient_CT_dir,  patient_ROI_type = rd.get_MAASTRO_CT_ROI_data(_path)
        # contour structure file
        contour_data    = util.get_struct_file(patient_CT_dir,patient_ROI_type)
        # ROI sequences
        contour_names   = util.get_roi_names(contour_data)
        # index for Gross Tumor Volume (GTV)
        contour_idx     = rd.get_ROI_index(contour_names, 'GTV-1')
        # path to CT images
        contour_imgs    = rd.get_MAASTRO_CT_directory(patient_CT_dir)
        # list of images and corresponding contours
        contour_arrays  = util.contour_to_pixel(_file=contour_data, _path=contour_imgs, _seq=contour_idx)
        print("#" + str(len(contour_arrays)) + " slices")

        _distant = int(_info[idx][d_col])
        _local   = int(_info[idx][l_col])
        _death   = 1 - int(_info[idx][s_col])
        _recc    = [_local, _distant, _death]
        print("metastasis: " + str(_recc))

        if write: rd.write_file_ROI(contour_arrays, _recc, '/radiomic-{:03d}-CT', idx+1)

def main():
    """
    python3 read_data.py -write True

    Inputs:
        -write (bool): True if you want to save desired pixel intensities, else False.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-write", type=str, required=True)
    args = parser.parse_args()

    _write = args.write

    if _write not in ("True", "False"): raise ValueError("-write must be \"True\" or \"False\"")

    get_data_clinic(_write == "True")

# execute main function
if __name__ == "__main__":
    main()

