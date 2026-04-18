# EEG/EMG Automated Sleep Scoring Classification Software adapted from SlumberNet by Jha, et al (2024) for use with the Chen Lab's data.
You can find the original publication here: https://doi.org/10.1038/s41598-024-54727-0.  
More information about the Chen's Lab research can be found here: https://sites.wustl.edu/yaochenlab/.  
Designed for use on WashU's Compute1 System, offered by WashU IT Research Infrastructure Services. More info can be found here: https://ris.wustl.edu/systems/scientific-compute-platform/.  
Note on the Python scripts: All model training-related scripts were originally designed to run on NVIDIA GPUs. Modifications may need to be made to run on CPUs only. These scripts are 2_slumbernet_k-fold_Adapted.py and 3_slumbernet_full_training_Adapted.py.  
All required packages are listed in model.requirements.txt.  
Label_epochs_by_group.py is no longer used; it is kept as a reference only.  
## Building and Pushing Docker Images using Dockerfiles
There are 2 Docker files in this repository: preprocessing.Dockerfile and train_model.Dockerfile. They can be used to build the corresponding Docker  Containers, which can then run on Compute1. Which Docker Image you use depends on the scripts that you want to run.  
If you want to run Compile_Voltage_and_Epoch_Label_Dataset.py, 1_slumbernet_preprocessing_Adapted.py, use preprocessing.Dockerfile. Your build command should look like the following:
```
docker build  -f preprocessing.Dockerfile -t username/container-name:tag directory .
```
**Note**: the "." at the end is intentional, otherwise you will get a build error.  
If you want to run 2_slumbernet_k-fold_Adapted.py or 3_slumbernet_full_training_Adapted.py, use train_model.Dockerfile *and* change the CMD.  
To push the Docker Image for use in Compute1, the command should look like the following:
```
docker push username/container-name:tag directory
```
## Running Jobs on Compute1
For all jobs submitted via the termnial or the shell via OpenOnDemand (OOD), make sure to run the following lines:
```
export STORAGE1=/storage1/fs1/yaochen/Active 
export LSF_DOCKER_VOLUMES="$HOME:$HOME $STORAGE1:$STORAGE1" 
```
## Preprocessing Steps
The first script you want to run for input into SlumberNet's preprocessing code is Compile_Voltage_and_Epoch_Label_Dataset.py.  
Before running this script, make sure to have all the data (*_EEGData.pkl and *_SSData.pkl) you want converted into one folder.  
Configure filepaths in both Compile_Voltage_and_Epoch_Label_Dataset.py and 1_slumbernet_preprocessing_Adapted.py before building the Docker Image.
Also make any desired modifications such as sampling rate, filter orders, etc., in 1_slumbernet_preprocessing_Adapted.py before building as well.   
Build and push the corresponding Docker Image using preprocessing.Dockerfile.  
To run on Compute1, the command in the ternminal should look like the following:
```
bsub -q general -R 'rusage[mem=16GB]' -a 'docker(username/container-name:tag directory)' python3 /Compile_Voltage_and_Epoch_Label_Dataset.py
```
Memory usage (rusage) can be altered as needed, though I found that 16 GB is about the minimium memory it needs for 18 experiments.  
After that first job completes, run 1_slumbernet_preprocessing_Adapted.py on Compute1 using the same Docker Image as before. The command line should look like the following:
```
bsub -q general -R 'rusage[mem=128GB, tmp=16GB]' -a 'docker(username/container-name:tag directory)' python3 /1_slumbernet_preprocessing_Adapted.py
```
Again, memory usage (rusage) can be altered as needed, though these are the values that I ended up using.
## Model Training Steps
Note: Due to time constraints, no full model training was performed so little modifications were made in 3_slumbernet_full_training_Adapted.py in comparision to the original code.  
For training and performing validation testing, use 2_slumbernet_k-fold_Adapted.py. For full model training use 3_slumbernet_full_training_Adapted.py.   
Configure desired filepaths and change parameters if needed/desired before building Docker Image. Make sure the CMD command on the last line (line 24) in train_model.Dockerfile reads the following:
```
CMD ["/opt/venv/bin/python3", "2_slumbernet_k-fold_Adapted.py"]
```
or
```
CMD ["/opt/venv/bin/python3", "3_slumbernet_full_training_Adapted.py"]
```
for full training.  
Build and push the corresponding Docker Image using train_model.Dockerfile. I would recommend building a separate container (using a different container name) to avoid any potential conflicts between images in the same container, particularly because this container will host a virtual Python environment inside of it.
To run on Compute1, the command in the ternminal should look like the following:
```
bsub -q general  -R 'gpuhost rusage[mem=40GB]' -gpu "num=3:gmodel=NVIDIAA100_SXM4_40GB" -a 'docker(username/container-name:tag directory)' /opt/venv/bin/python3 /2_slumbernet_k-fold_Adapted.py
```
For full model training, replace 2_slumbernet_k-fold_Adapted.py with 3_slumbernet_full_training_Adapted.py.  
As with preprocessing, memory usage (rusage) can be altered as needed. I used these particular GPUs because no other ones were available. The ones that are closer to the ones that the original publication of SlumberNet used are the TeslaV100_SXM2_32GB in Compute1.