##############################
FROM ubuntu:20.04

### ENV
ENV DEBIAN_FRONTEND=noninteractive

### Localtime
ENV LC_ALL C.UTF-8
ENV TimeZone=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
RUN apt-get update -y --fix-missing && \
    apt-get install -y --no-install-recommends \
    tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata

### Install OS Package
RUN apt-get update -y --fix-missing && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \ 
    curl \
    clang \
    ca-cacert \
    cmake \
    git \
    gcc \
    g++ \
    gnupg \
    iputils-ping \
    libssl-dev \
    libssh-dev \
    make \
    nano \
    openssl \
    openssh-server \
    pkg-config \
    unzip \
    wget \
    zip \
    && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

### Install Python
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-numpy \
    && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

### Update Python3 pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip3 install --upgrade pip && \
    rm get-pip.py

### Install Web Framework
RUN apt-get -y update && \
    pip3 --no-cache-dir install \
    fastapi \
    uvicorn \
    pydantic \
    typing \
    python-multipart \
    websockets \
    gunicorn \
    email-validator \
    && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

##############################
### Edit Software Link Python2 to Python3
RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python
### Create Work Path
WORKDIR /home
### Clean Package
RUN apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/
##############################

COPY ./Main4Py /Main4Py
WORKDIR "/Main4Py"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]]
EXPOSE 80
EXPOSE 9090
##############################
LABEL Master=ThanatosHsiao Version=2022.07
##############################
