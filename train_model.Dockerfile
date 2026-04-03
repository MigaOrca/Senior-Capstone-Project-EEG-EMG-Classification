# trying to figure out correct packages/image to use, do not use this yet
FROM nvidia/cuda:13.2.0-cudnn-runtime-ubuntu22.04 
ENV DEBIAN_FRONTEND=noninteractive


ARG PYTHON_VERSION=python3.12
COPY model.requirements.txt /model.requirements.txt
# Install the application dependencies
RUN pip install --no-cache-dir -r /model.requirements.txt -U
COPY \
    2_slumbernet_k-fold_Adapted.py
    3_slumbernet_full_training_Adapted.py /