#!/bin/bash -e

DOCKER_BUILDKIT=1
sudo docker build --no-cache -t rce-cmpairs .
