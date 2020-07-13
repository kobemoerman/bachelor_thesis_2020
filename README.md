# Autoencoders for head and neck cancer prognosis.

First, the data needs to be extracted from the database. This is done in the "data_preprocessing" folder. There are two sets of data which require distinct argument parsing:
* The MAASTRO file is compiled by: python3 data_MAASTRO.py -write (bool). The -write argument is responsible for saving the extracted values.
* The MCGILL file is compiled by: python3 data_MCGILL.py -write (bool) -inst CHUM CHUS HGJ HMR. In this case the -inst argument allows the user to specify which clinical institutions to extract data from.

Then, the data has to undergo a pre-processing phase in order to feed this one to a neural network.
* The file is compiled by: python3 upload_data.py -slices (int). The -slices argument represents how many slices need to be extracted for each patient. The result is then saved to a new folder.

Each neural network was create and executed in Google Colab. As such, the prepared data needs to be uploaded to Google Drive to access it.
