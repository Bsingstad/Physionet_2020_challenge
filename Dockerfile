FROM python:3.7.3-slim

## The MAINTAINER instruction sets the Author field of the generated images
MAINTAINER "Bjorn-Jostein Singstad <b.j.singstad@fys.uio.no>"

# ENV CURRENT-VERSION="v0.5.1-tracing"
RUN wget https://github.com/github/git-lfs/releases/download/v0.5.1-tracing/git-lfs-linux-amd64-0.5.1.tar.gz
RUN tar -xvf git-lfs-linux-amd64-0.5.1.tar.gz
RUN cd git-lfs-0.5.1
RUN /bin/bash install.sh

## DO NOT EDIT THESE 3 lines
RUN mkdir /physionet
COPY ./ /physionet
WORKDIR /physionet

## Install your dependencies here using apt-get etc.

## Do not edit if you have a requirements.txt
RUN pip install -r requirements.txt
