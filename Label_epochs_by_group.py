# Code to sort data into subject-wide folds, not epoch sorted

import numpy as np

# Input directory
input_directory = '/storage1/fs1/yaochen/Active/Emily-Senior-Capstone/EEG_Data_Preprocessed/'

# master_epoch_array BEFORE deletion
master_epoch_array = np.load(input_directory + "eeg_epoch_data_no_scaling_all.npy")

A_list = np.where(np.all(master_epoch_array == np.array([1,1,1]), axis=1))[0]
print(A_list)

orig_counts = [
    43181, 21581, 36881, 21581, 21581, 43181, 43181, 21581, 
    21581, 43181, 43181, 32381, 43181, 21581, 21581, 43181, 43181, 43181
]

boundaries = np.cumsum([0] + orig_counts)

removed_per_experiment = []
for i in range(len(orig_counts)):
    start = boundaries[i]
    end = boundaries[i+1]
    removed = A_list[(A_list >= start) & (A_list < end)]
    removed_per_experiment.append(removed)

final_counts = [
    orig_counts[i] - len(removed_per_experiment[i])
    for i in range(len(orig_counts))
]

groups = np.concatenate([
    np.full(final_counts[i], i)
    for i in range(len(final_counts))
])

np.save(f"{input_directory}/recording_id_array.npy", groups)
assert len(groups) == len(master_epoch_array) - len(A_list)
master_epoch_array_final = np.load(input_directory + "epoch_input_array.npy")
assert len(groups) == len(master_epoch_array_final)