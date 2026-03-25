# This Python script converts *_EEGData.pkl into usable inputs for 1_slumbernet_preprocessing_Adapted
# Extracts the first two columns of *_EEGData.pkl which are the EMG column (1) and the frontal EEG column (2)

# Requires all files to be used in dataset to be compiled into one folder

### ---- Load libraries ---- ###
import pandas as pd
import numpy as np
import os

# Input directory
input_dir =  '/home/projects/eeg_deep_learning/eeg_data_raw/' # to be changed
output_dir = '/home/projects/eeg_deep_learning/eeg_dataset/' # to be changed
# Create two empty lists to store the filenames
voltage_file_list = []
epoch_file_list = []

for filename in os.listdir(input_dir):
    if filename.endswith("EEGData.pkl"):
        # Add the filename to list1
        voltage_file_list.append(filename)
    elif filename.endswith("SSData.pkl"):
        # Add the filename to list2
        epoch_file_list.append(filename)

for file_number in range(0,len(voltage_file_list)):
    current_voltage_file_name = voltage_file_list.loc[file_number, "voltage_file"]
    voltage_file_name = f'{input_dir}/{current_voltage_file_name}'
    voltages = pd.read_pickle(voltage_file_name)
    desired_voltages = voltages.reindex(columns = ['EMG','EEG Frontal']) # ask Lizze about this
    # look into how Jha formatted their .txt files