# Unittests for salt-call CLI

from __future__ import unicode_literals
import salt_test.cli
import unittest
import mock
import sys
import StringIO

class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def fake_exit(self, retcode=0):
        print(retcode)

    def test_main_noargs(self):
        with self.assertRaises(SystemExit) as on_exit:
            argv = ['salt-test']
            with mock.patch('sys.argv', argv),\
                    mock.patch('sys.stderr', StringIO.StringIO()) as stderr,\
                    mock.patch('sys.stdout', StringIO.StringIO()) as stdout:
                salt_test.cli.main()
            self.assertEqual(salt_test.cli.__doc__ in stdout.getvalue())
        self.assertEqual(on_exit.exception.code, 2)

    def test_main_help(self):
        with self.assertRaises(SystemExit) as on_exit:
            argv = ['salt-test', '-h']
            with mock.patch('sys.argv', argv),\
                    mock.patch('sys.stdout', StringIO.StringIO()) as stdout:
                salt_test.cli.main()
            self.assertEqual(salt_test.cli.__doc__ in stdout.getvalue())
        self.assertEqual(on_exit.exception.code, 0)

    def test_main_help_long(self):
        with self.assertRaises(SystemExit) as on_exit:
            argv = ['salt-test', '--help']
            with mock.patch('sys.argv', argv),\
                    mock.patch('sys.stdout', StringIO.StringIO()) as stdout:
                salt_test.cli.main()
            self.assertEqual(salt_test.cli.__doc__ in stdout.getvalue())
        self.assertEqual(on_exit.exception.code, 0)

    def test_main_success(self):
        with self.assertRaises(SystemExit) as on_exit:
            argv = ['salt-test', 'test.state.foobar']
            with mock.patch('sys.argv', argv),\
                    mock.patch('salt_test.cli.run_tests', return_value=True) as run_tests:
                salt_test.cli.main()
        self.assertEqual(on_exit.exception.code, 0)
        run_tests.assert_called_with(['test.state.foobar'])

    def test_main_failure(self):
        with self.assertRaises(SystemExit) as on_exit:
            argv = ['salt-test', 'test.state.foobar']
            with mock.patch('sys.argv', argv),\
                    mock.patch('salt_test.cli.run_tests', return_value=False) as run_tests:
                salt_test.cli.main()
        self.assertEqual(on_exit.exception.code, 1)
        run_tests.assert_called_with(['test.state.foobar'])

