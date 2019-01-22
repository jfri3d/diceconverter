FROM thinkwhere/gdal-python:3.6-ubuntu

MAINTAINER Joshua Friedman <j.friedman@kigroup.de>

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# This will install latest version of GDAL
RUN pip3 install GDAL>=2.2.4
RUN pip3 install click==6.7 qrcode giphypop
RUN pip3 install Pillow numpy
