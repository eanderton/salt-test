# forked from https://github.com/dawidmalina/docker-salt-environment/blob/master/slave-ubuntu-16.04/Dockerfile
#
# Dockerfile for running salt-test examples in this directory.
#
FROM ubuntu:16.04

ENV SALT_VERSION=2017.7.1

RUN apt-get install -y 

RUN apt-get update \
  && apt-get install -y vim-nox curl software-properties-common \
  && curl -L https://repo.saltstack.com/apt/ubuntu/16.04/amd64/archive/${SALT_VERSION}/SALTSTACK-GPG-KEY.pub | apt-key add - \
  && echo "deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/archive/${SALT_VERSION} xenial main" > /etc/apt/sources.list.d/saltstack.list \
  && add-apt-repository ppa:duggan/bats \
  && apt-get update \
  && apt-get install -y libdbus-1-3 libnih-dbus1 sudo software-properties-common iputils-ping apt-transport-https debian-archive-keyring \
  && apt-get install -y salt-minion=${SALT_VERSION}* \
  && apt-get install -y git bash bats python-pip

RUN git clone https://github.com/eanderton/salt-test.git \
  && cd salt-test \
  && ls -alF \
  && python setup.py --verbose install \
  && find / -iname salt-test

WORKDIR /root

#ENTRYPOINT ["/bin/bash", "-l", "-c"]

