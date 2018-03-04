#!/bin/bash

# run one test battery inside a container
docker run \
  --name run-salt-test \
  --volume $(pwd):/root \
  ubuntu-salt-test \
  salt-test tests.install

docker container rm run-salt-test
