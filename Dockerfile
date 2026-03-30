FROM python:3.14

# Install the application dependencies
RUN pip install --no-cache-dir -U numpy pandas scipy sklearn tensorflow seaborn matplotlib
COPY Compile_Voltage_and_Epoch_Label_Dataset.py /