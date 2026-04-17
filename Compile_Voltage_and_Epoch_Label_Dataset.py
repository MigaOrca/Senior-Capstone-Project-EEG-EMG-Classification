# This Python script converts *_EEGData.pkl and *_SSData.pkl files into usable inputs for 1_slumbernet_preprocessing_Adapted
# Requires all files to be used in dataset to be compiled into one folder. Change filepaths as needed.
# It first extracts the first two columns of each *_EEGData.pkl in the given directory which are the Column 1: "EMG" and Column 2: "EEG (Frontal Channel)"
# After all the *_EEGData.pkl are covnerted into .txt, all of the labels for Wake, NREM, and REM are converted to match SlumberNet's labelling 
# # and are then converted into .txt files
# Each EEG file pair takes ~1 min/GB

### ---- Load libraries ---- ###
import pandas as pd
import os

### ---- Compliation of files to form dataset ---- ###
# directories
input_dir =  '/storage1/fs1/yaochen/Active/Emily-Senior-Capstone/Compilation_Data_Folder' # change if needed
output_dir = '/storage1/fs1/yaochen/Active/Emily-Senior-Capstone/EEG_Training_Data' # change if needed

# makes new output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Creates two lists to store the voltage and epoch filenames respectively
voltage_file_list = [filename for filename in os.listdir(input_dir) if filename.endswith("EEGData.pkl")]
epoch_file_list = [filename for filename in os.listdir(input_dir) if filename.endswith("SSData.pkl")]

### ---- Voltage file processing ---- ###
for file_number in range(0,len(voltage_file_list)):
    current_voltage_file_name = voltage_file_list[file_number]
    voltage_file_name = f'{input_dir}/{current_voltage_file_name}'
    voltages = pd.read_pickle(voltage_file_name)
    # extracts Column 1: "EMG" and Column 2: "EEG (Frontal Channel)" from *._EEGData.pkl. Can be modified to include Column 3: "EEG (Hippocampal Channel)"
    desired_voltages = voltages.reindex(columns = ['EMG','EEG (Frontal Channel)'])
    
    # rename columns in voltage DataFrame to match SlumberNet Names
    desired_voltages.rename(columns={'EMG': 'emg_voltage', 'EEG (Frontal Channel)': 'eeg_voltage'}, inplace=True)
    # remove .pkl extension
    new_voltage_file_name = current_voltage_file_name.split(".", 1)
     # export voltage DataFrame to text file while keeping column format (doesn't keep  index column but keeps header; change to true if want to keep)
    voltage_pathname = os.path.join(output_dir, new_voltage_file_name[0] + '.txt')
    desired_voltages.to_csv(voltage_pathname, sep='\t', index=False)

### ---- Epoch file processing ---- ###
for file_number in range(0,len(epoch_file_list)):
    current_epoch_file_name = epoch_file_list[file_number]
    epoch_file_name = f'{input_dir}/{current_epoch_file_name}'
    epochs = pd.read_pickle(epoch_file_name)
    
    # rename columns in epoch DataFrame to match SlumberNet Names
    epochs.rename(columns={'Sleep States': 'sleep_stage', 'Sleep States Time (s)': 'datetime'}, inplace=True)
    # Replacing labels of 1, 2, 3 (1 = Wake, 2 = NREM, 3 = REM) to match SlubmerNet's labels: Wake(W), NREM(N), REM(R)
    epochs.replace(1.0, 'W', inplace = True)
    epochs.replace(2.0, 'N', inplace = True)
    epochs.replace(3.0, 'R', inplace = True)
    # remove .pkl extension
    new_epoch_filename = current_epoch_file_name.split(".", 1)
    # export epoch DataFrame to text file while keeping column format (doesn't keep  index column but keeps header; change to true if want to keep)
    epoch_pathname = os.path.join(output_dir, new_epoch_filename[0] + '.txt')
    epochs.to_csv(epoch_pathname, sep='\t', index=False)