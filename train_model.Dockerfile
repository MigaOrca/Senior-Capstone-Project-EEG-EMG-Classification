FROM nvidia/cuda:13.2.0-cudnn-devel-ubuntu24.04

# Set non-interactive mode for apt and install basic dependencies, ensuring Python 3.12 installation through deadsnakes PPA
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
software-properties-common build-essential wget curl git ca-certificates && \
add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
apt-get install -y --no-install-recommends python3.12 python3.12-dev python3.12-distutils && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.12 get-pip.py && rm get-pip.py

# Install the SlumberNet dependencies
COPY model.requirements.txt /model.requirements.txt
RUN pip install --no-cache-dir -r /model.requirements.txt -U
COPY 2_slumbernet_k-fold_Adapted.py 3_slumbernet_full_training_Adapted.py /