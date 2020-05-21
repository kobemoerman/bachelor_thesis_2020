import os
import argparse
import xdrlib
import pandas as xlsx

import utility as util
import clinic as data
import read_data as rd

patient = 0

home_dir     = os.getcwd() + "/database/Head-Neck-PET-CT"
info_xlsx    = os.getcwd() + "/database/INFOclinical_HN_Version2_30may2018.xlsx"
contour_xlsx = os.getcwd() + "/database/INFO_GTVcontours_HN.xlsx"

def get_data_clinic(clinic, write):
    """
    Retrive the ROI and corresponding CT images. Write the pixel intensities to a new directory.

    Inputs:
        clinic (str): clinic to retrieve data from.
        write (bool): determine whether to write pixel intensities to new directory
    """
    global patient

    _inst = data.get_clinic(clinic)

    # clinic parameters
    _patient    = _inst.prefix
    _size       = _inst.size
    _outlier    = _inst.outlier

    # load excel information file for current study
    _info = xlsx.read_excel(info_xlsx, sheet_name=clinic)
    loco_col  = _info['Locoregional'].tolist()
    dist_col  = _info['Distant'].tolist()
    death_col = _info['Death'].tolist()

    # load excel contour file for current study
    _contour = xlsx.read_excel(contour_xlsx, sheet_name=clinic)
    patient_col = _contour['Patient'].tolist()
    ROI_col     = _contour['Name GTV Primary'].tolist()

    for idx, _patient in enumerate(patient_col):
        # ignore any outliers
        if int(_patient[8:]) in _outlier: continue

        print("Processing patient " + _patient)
        _path = home_dir + '/' + _patient

        # path to the ROI files
        patient_ROI_dir, patient_ROI_type = rd.get_MCGILL_ROI_data(_path,_inst)
        # contour structure file
        contour_data    = util.get_struct_file(patient_ROI_dir,patient_ROI_type)
        # ROI sequences
        contour_names   = util.get_roi_names(contour_data)
        # index for Gross Tumor Volume (GTV)
        contour_idx     = rd.get_ROI_index(contour_names, ROI_col[idx])
        # path to CT images
        contour_imgs    = rd.get_MCGILL_CT_data(_path)
        # list of images and corresponding contours
        contour_arrays  = util.contour_to_pixel(_file=contour_data, _path=contour_imgs, _seq=contour_idx)

        print("#" + str(len(contour_arrays)) + " slices")

        _recc = int(loco_col[idx] or dist_col[idx])

        print("metastasis: " + str(_recc))

        patient = patient + 1
        if write: rd.write_file_ROI(contour_arrays, _recc, '/1-{:03d}-CT', patient)


def main():
    """
    python3 read_data.py -write True -inst CHUM CHUS HGJ HMR

    Inputs:
        -write (bool): True if you want to save desired pixel intensities, else False.
        -inst (list): clinic to read data from.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-write", type=str, required=True)
    parser.add_argument("-inst", nargs='+', required=True)
    args = parser.parse_args()

    _write = args.write

    if _write not in ("True", "False"): raise ValueError("-write must be \"True\" or \"False\"")

    for _inst in args.inst:
        get_data_clinic(_inst, _write == "True")

# execute main function
if __name__ == "__main__":
    main()

