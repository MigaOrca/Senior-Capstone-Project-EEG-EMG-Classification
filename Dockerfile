FROM python:3.12

# Install the application dependencies
RUN pip install --no-cache-dir -U numpy pandas scipy scikit-learn tensorflow[and-cuda] seaborn matplotlib
COPY Compile_Voltage_and_Epoch_Label_Dataset.py /