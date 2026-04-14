FROM python:3.12
# Install SlumberNet Preprocessing Dependencies
RUN pip install --no-cache-dir -U numpy pandas scipy
# Adding SlumberNet Preprocessing Files to Dockerfile
COPY Compile_Voltage_and_Epoch_Label_Dataset.py 1_slumbernet_preprocessing_Adapted.py Label_epochs_by_group.py /