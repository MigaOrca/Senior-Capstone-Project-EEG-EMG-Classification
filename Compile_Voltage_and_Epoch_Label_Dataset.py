# This Python script converts *_EEGData.pkl into usable inputs for 1_slumbernet_preprocessing_Adapted
# Extracts the first two columns of *_EEGData.pkl which are the Column 1: "EMG" and Column 2: "EEG (Frontal Channel)"

# Requires all files to be used in dataset to be compiled into one folder

### ---- Load libraries ---- ###
import pandas as pd
import numpy as np
import os

### ---- Compliation of files to form dataset ---- ###

# directories
input_dir =  '/Volumes/yaochen/Active/Emily-Senior-Capstone/Compilation_Data_Folder'
output_dir = '/Volumes/yaochen/Active/Emily-Senior-Capstone/EEG_Training_Data'

# makes new output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
    current_voltage_file_name = voltage_file_list[file_number]
    voltage_file_name = f'{input_dir}/{current_voltage_file_name}'
    voltages = pd.read_pickle(voltage_file_name)
    # extracts Column 1: "EMG" and Column 2: "EEG (Frontal Channel)" from *._EEGData.pkl. Can be modified to include Column 3: "EEG (Hippocampal Channel)"
    desired_voltages = voltages.reindex(columns = ['EMG','EEG (Frontal Channel)'])
    
    # rename columns in voltage DataFrame to match SlumberNet Names
    desired_voltages.rename(columns={'EMG': 'emg_voltage', 'EEG (Frontal Channel)': 'eeg_voltage'}, inplace=True)
    # remove .pkl extension
    voltage_file_name = voltage_file_name.split(".", 1)
    new_voltage_filename = voltage_file_name[0] + '.txt'
    
    # export voltage DataFrame to text file (doesn't keep header row and index column; change to true if want to keep)
    path = output_dir + "/" + new_voltage_filename
    with open(path, 'a') as f:
        df_string = desired_voltages.to_string(header=False, index=False)
        f.write(df_string)

for file_number in range(0,len(epoch_file_list)):
    current_epoch_file_name = epoch_file_list[file_number]
    epoch_file_name = f'{input_dir}/{current_epoch_file_name}'
    epochs = pd.read_pickle(epoch_file_name)
    
    # rename columns in epoch DataFrame to match SlumberNet Names
    epochs.rename(columns={'Sleep States': 'sleep_stage', 'Sleep States Time (s)': 'datetime'}, inplace=True)
    # Replacing labels of 1, 2, 3 (1 = Wake, 2 = NREM, 3 = REM) to match SlubmerNet's labels: Wake(W), NREM(N), REM(R)
    epochs.replace(1.0, 'W')
    epochs.replace(2.0, 'N')
    epochs.replace(3.0, 'R')
    # remove .pkl extension
    epoch_file_name = epoch_file_name.split(".", 1)
    new_epoch_filename = epoch_file_name[0] + '.txt'

    # export epoch DataFrame to text file (doesn't keep header row and index column; change to true if want to keep)
    path = output_dir + "/" + new_epoch_filename
    with open(path, 'a') as f:
        df_string = epochs.to_string(header=False, index=False)
        f.write(df_string)