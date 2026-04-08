FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04
# Set non-interactive mode for apt and install basic dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git ca-certificates curl \
# Install Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \ 
    python-is-python3 \
    python3-pip \
    python3-dev \
    python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Creating Virtual Environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Install the SlumberNet Dependencies
COPY model.requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -Ur model.requirements.txt
COPY 2_slumbernet_k-fold_Adapted.py 3_slumbernet_full_training_Adapted.py /
# Change 2_slumbernet_k-fold_Adapted.py to 3_slumbernet_full_training_Adapted.py for full model training
CMD ["/opt/venv/bin/python3", "2_slumbernet_k-fold_Adapted.py"]