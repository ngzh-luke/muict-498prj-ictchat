# Start from the official Ubuntu base image
FROM ubuntu:22.04

# Set the current working directory to /home/app
WORKDIR /home/app

# Uncomment and fill in your account if you are working under MU network
# ENV http_proxy "http://<USER>:<PASSWD>@proxy-sa.mahidol:8080"
# ENV https_proxy "http://<USER>:<PASSWD>@proxy-sa.mahidol:8080"
# ENV ftp_proxy "http://<USER>:<PASSWD>@proxy-sa.mahidol:8080"
# ENV no_proxy "localhost,127.0.0.1,::1"

# Project files from the local directory to the image
COPY src/ /home/app
COPY requirements.txt /home/app/
COPY .env /home/app/

# force run using bash
SHELL ["/bin/bash", "-c"]

# Update software in Ubuntu
RUN apt-get update 
# install necessary lib
RUN apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    vim \
    bzip2 \
    ca-certificates \
    libsm6 \
    libxext6

# Setup Miniconda
ENV PATH /opt/conda/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Install Python packages
RUN pip --no-cache-dir install --upgrade pip
RUN pip --no-cache-dir install -r /home/app/requirements.txt

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]