#!/usr/bin/env python3

import os
import pexpect
import random
import re
import string
import sys
from tempfile import mkstemp
import unittest

class TestPractica2_1(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        cls.my_dir=os.path.dirname(os.path.realpath(__file__))
        cls.script_name=os.path.realpath('{}/../practica_2/practica2_1.sh'.format(cls.my_dir))
        cls.timeout=5

    def setUp(self):
        self.child = pexpect.spawn('/bin/bash {}'.format(self.script_name), encoding='utf-8')
        self.pass_test = True
        # self.child.logfile = sys.stdout

        # create a temporal file
        self.tmp_handle, self.tmp_name = mkstemp(prefix='with_space ')

    def tearDown(self):
        self.child.terminate(force=True)
        # delete file
        os.close(self.tmp_handle)
        os.unlink(self.tmp_name)

    def test_shebang(self):
        with open(self.script_name) as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None), msg='Invalid shebang')

    def test_no_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ', timeout=self.timeout)
        os.chmod(self.tmp_name, 0o000)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: ---\r\n'.format(self.tmp_name), timeout=self.timeout)
        except:
            self.pass_test = False
        self.assertTrue(self.pass_test, msg='Incorrect permit. Expected value: ---')

    def test_exec_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ', timeout=self.timeout)
        os.chmod(self.tmp_name, 0o100)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: --x\r\n'.format(self.tmp_name), timeout=self.timeout)
        except:
            self.pass_test = False
        self.assertTrue(self.pass_test, msg='Incorrect permit. Expected value: --x')

    def test_read_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ', timeout=self.timeout)
        os.chmod(self.tmp_name, 0o400)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: r--\r\n'.format(self.tmp_name), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Incorrect permit. Expected value: r--')

    def test_read_write_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ', timeout=self.timeout)
        os.chmod(self.tmp_name, 0o600)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: rw-'.format(self.tmp_name), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Incorrect permit. Expected value: rw-')

    def test_read_write_exec_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0o700)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: rwx'.format(self.tmp_name))
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Incorrect permit. Expected value: rwx')

    def test_read_invalid_filename(self):
        fname=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))
        while os.path.isfile(fname):
            fname=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))

        try:
            self.child.expect('Introduzca el nombre del fichero: ', timeout=self.timeout)
            self.child.sendline(fname)
            self.child.expect('{} no existe'.format(fname), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Invalid output. Expected output: {} no existe'.format(fname))

if __name__ == "__main__":
    unittest.main()
