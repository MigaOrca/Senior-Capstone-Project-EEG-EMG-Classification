FROM python:3.14

# Install the application dependencies
# need to fix tensorflow, and may need to downgrade to 3.13
RUN pip install --no-cache-dir -U numpy pandas scipy scikit-learn tensorflow seaborn matplotlib
COPY Compile_Voltage_and_Epoch_Label_Dataset.py /