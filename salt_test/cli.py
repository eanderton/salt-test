#!/usr/bin/python
"""Salt unittest runner.  Runs .sls files with an isolated configuration
along with embedded jinja data.  Supports pillar and grain overrides,
and pass/fail/changed count assertions.  

Overall, this tool is indented to close a gap between `salt-call --local`
and `salt * --test`.  Tests are run live (no --test) locally, in the 
current environment, using a single-sls-as-test scheme, instead of 
reconfiguring the salt-minion configuration tree for each test.

In any test .sls file, if the jinja variable `testconfig` exists, it is
parsed and consumed as configuration for the containing salt run.

The test .sls itself may be any valid set of salt states, but is best
implemented as one or more include statements for code under test. 
Additional assertions like test scripts can also be run by using
`cmd.run`, to futher verify the results of the run.

This tool will apply test states in-situ just like salt-call.  For
best results, run inside an isolated environment such as a Docker
container or dedicated virtual machine.
"""

from __future__ import unicode_literals, print_function
import sys
import os
import json
import argparse
import salt.config
from backports.tempfile import TemporaryDirectory
from salt.cli.caller import BaseCaller
from salt.output import display_output


testconfig_defaults = {
    'pillar': {},
    'grains': {},
    'assert': {
        'passed': None,
        'changed': None,
        'failed': 0,
        'total': None,
    },
}


def dict_merge(a, b, path=None):
    """ Merges b into a 
    """

    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                dict_merge(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a


def local_salt_call(fun, *args, **kwargs):
    """ Pythonic equivalent to `salt-call --local ...`.  Args and kwargs
        are pased to the provided function `fun`, as though they were 
        passed on the command line.
    """

    # pull the grains out of kwargs if applicable
    grains = {}
    if 'grains' in kwargs:
        grains = kwargs['grains']
        del kwargs['grains']

    # establish cache dir
    with TemporaryDirectory('salt-test-cache') as cachedir:
        # build configuration around a non-existent config file for a 'local' run
        # NOTE: kwargs are reformatted as 'k=v' pairs as though they were passed on
        # the commandline
        opts = salt.config.minion_config('/dev/null')
        opts.update({
            'id': 'local',
            'file_client': 'local',
            'cachedir': cachedir,
            'local': True,
            'grains': grains,
            'fileserver_backend': ['roots'],
            'file_roots': { 'base': [os.getcwd()] },
            'fun': fun,
            'arg': list(args) + ['{}={}'.format(k,v) for k,v in kwargs.iteritems()],
            'retcode_passthrough': True,
        })
        #print(json.dumps(opts, indent=4))
        return BaseCaller(opts).call()


def extract_testconfig(test_unit_sls):
    """ Extract any declation of 'testconfig' from the test .sls file.    
        The configuration data is merged with the defaults, to yield a
        fully configured set.
    """

    script = "{% import '" + test_unit_sls + "' as ctx %}" +\
	"{{ ctx.__dict__.get('testconfig', {}) }}"
    embed_testconfig = local_salt_call('slsutil.renderer', string=script)['return']
    if not isinstance(embed_testconfig, dict):
        embed_testconfig = {}
    return reduce(dict_merge, [{}, testconfig_defaults, embed_testconfig])


def state_apply(test_unit, testconfig):
    """ Mimics `salt-call state.apply` with grains and pillar overrides. 
    """

    grains = testconfig['grains']
    pillar_json = json.dumps(testconfig['pillar'])
    return local_salt_call('state.apply', test_unit, grains=grains, pillar=pillar_json)


def output_run(run_data, name):
    """ Outputs a salt run to stdout, in the usual SaltStack style.
    """

    print(json.dumps(run_data, indent=4))
    ret = run_data.get('return', {})
    display_output(
        {name: ret}, 
	out=run_data.get('out', 'nested'),
	opts = salt.config.minion_config('/dev/null'))


def eval_assertions(run_data, test_unit, testconfig):
    """ Evaluates pass/change/fail/total count assertions against a run, 
        as defined in testconfig.
    """

    tests_passed = True
    passed = 0
    failed = 0
    changed = 0
    for name, entry in run_data['return'].iteritems():
        if entry['result']:
            passed = passed + 1 
        else:
            failed = failed + 1
        if entry['changes'] != {}:
            changed = changed + 1 

    assert_passed = testconfig['assert']['passed']
    assert_changed = testconfig['assert']['changed']
    assert_failed = testconfig['assert']['failed']
    assert_total = testconfig['assert']['total']
    total = passed + failed

    def assert_test(name, expect, value): 
        if expect is not None and expect != value:
            print('FAIL ({}): expected {} {} states; got {} instead'\
                .format(test_unit, name, expect, value))
            tests_passed = False

    assert_test('passed', assert_passed, passed)
    assert_test('changed', assert_changed, changed)
    assert_test('failed', assert_failed, failed)
    assert_test('total', assert_total, total)

    return tests_passed


def run_tests(tests):
    tests_passed = True

    for test_unit in tests:
        # get testconfig by evaluating the sls file and extracting jinja vars
        parts = [os.getcwd()] + test_unit.split('.')
        test_unit_sls = os.path.join(*parts) + '.sls'
        testconfig = extract_testconfig(test_unit_sls)
        #print(json.dumps(testconfig, indent=4))

        # run the test
        run_data = state_apply(test_unit, testconfig)
        output_run(run_data, test_unit)
        #print(json.dumps(run_data, indent=4))
        tests_passed = tests_passed and eval_assertions(run_data, test_unit, testconfig)

    return tests_passed


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    parser.add_argument('test_states', metavar='test-states', nargs='+', help='states to run')
    
    args = parser.parse_args()
    if run_tests(args.test_states):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
