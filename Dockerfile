FROM ubuntu:22.04

# Avoid interactive prompts for geographic area / timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update -y
RUN apt-get install -y openssh-client
RUN apt-get install -y python3
RUN apt-get install -y vim
RUN apt-get install -y git
RUN apt-get install -y infernal

COPY .vimrc /root
COPY bash_include /root

RUN cat /root/bash_include >> /root/.profile
RUN cat /root/bash_include >> /root/.bashrc

RUN git clone https://github.com/rcedgar/cmpairs.git

RUN chmod +x cmpairs/*.bash cmpairs/*.py
