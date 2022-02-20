FROM ubuntu:22.04

# Avoid interactive prompts for geographic area / timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update -y
RUN apt-get install -y wget
RUN apt-get install -y openssh-client
RUN apt-get install -y python3
RUN apt-get install -y vim
RUN apt-get install -y git
RUN apt-get install -y build-essential
RUN apt-get install -y gcc-11 g++-11
RUN apt-get install -y emboss
RUN apt-get install -y infernal

RUN wget https://github.com/ViennaRNA/ViennaRNA/releases/download/v2.5.0/ViennaRNA-2.5.0.tar.gz
RUN tar -zxf ViennaRNA-2.5.0.tar.gz
RUN cd ViennaRNA-2.5.0/ && ./configure && make && make install

COPY .vimrc /root
COPY bash_include /root

RUN cat /root/bash_include >> /root/.profile
RUN cat /root/bash_include >> /root/.bashrc
