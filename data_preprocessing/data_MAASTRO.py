import os
import csv
import argparse

import utility as util
import read_data as rd

# tumor location (B)
site_col = 1
# patient age (C)
age_col = 2
# cancer T stage (G)
t_stage = 6
# cancer N stage (H)
n_stage = 7
# event overall survival (Q)
surv_col = 16
# event local recurrence (U)
loco_col = 20
# event distant metastasis (Y)
dist_col = 24

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

        # clinical data
        data = _info[idx]
        recurrence = [int(data[loco_col]), int(data[dist_col]), 1 - int(data[surv_col])]
        clinical   = [data[age_col], data[site_col], data[t_stage], data[n_stage]]

        if write: rd.write_file_ROI(contour_arrays, recurrence, clinical, '/radiomic-{:03d}-CT', idx+1)

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

