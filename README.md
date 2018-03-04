salt-test
-----

A test-runner for salt formulas, using salt.  This Python module
installs as a library and a script for easy use:

```
salt-test [options] test-state [test-state...]
```

Tests are conducted in an isolated masterless mode that does
not depend on any centralized configuration under the stock
install directories.  In most cases, tests can be conducted
using a single file outside the salt formula itself, much
like a Python unit-test.


Installation
-----

salt-test depends on the `salt` library, which in turn requires
`zmq`.  On a fresh install, you may need to install headers and
library dependencies for both salt and libzmq.

```
python setup.py install
```


Test States
-----

A test state is a salt-state that includes other states under
test and/or runs additional verfication states to assert
the system state. 

One feature peculiar to salt-test is that it looks for the
presence of a `testconfig` jinja variable in the test-state
file.  This is calculated before lowstate on a separate pass,
and is used to mock pillar data and grains.  It is also used
to assert the pass/fail/changed counts of the run itself.


The testconfig Section
-----
TBD


Development
-----

The setuptools script for this project provides a `develop` target 
that will install the development depenencies into the current
environment.  It is strongly recommended that the developer
establish a virtualenv before proceeding.

This will also require the installation requirements mentioned
in the Installation section above.

```
pyvenv env
. env/bin/activate
python setup.py develop
```


