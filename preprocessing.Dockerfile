FROM python:3.12

# Install the application dependencies
RUN pip install --no-cache-dir -U numpy pandas scipy
COPY Compile_Voltage_and_Epoch_Label_Dataset.py 1_slumbernet_preprocessing_Adapted.py /