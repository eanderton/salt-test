Docker Isolation Example
-----

This is example of how to conduct tests, using salt-test and
Docker, for isolating test runs from the enclosing environment.

Tests are stored in the `tests` subdirectory.  These include
code under the `mymodule` formula which is the code under test
in this example.

These docs assume that superuser is required to talk to Docker.
If that is not the case for your system, please disregard the 
use of `sudo` below.


1. Build Test Container
-----

The test environment will need salt-test installed to run the 
test .sls file.  In addition, this adds BATS as the tests in
this suite use it to verify details of the salt run.

```
sudo ./docker-build.sh
```

2. Run The Test Suite
-----

The complete battery of tests in the suite are all stored in
run-test.sh.


```
sudo ./run-test.sh
```
