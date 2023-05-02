#!/usr/bin/env python3

import os
import pexpect
import random
import re
from stat import S_ISREG, ST_MODE, S_IXUSR
import string
import sys
import unittest

class TestPractica2_4(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Find script directory and store its name in a variable """
        cls.my_dir=os.path.dirname(os.path.realpath(__file__))
        cls.script_name=os.path.realpath('{}/../practica_2/practica2_4.sh'.format(cls.my_dir))
        cls.timeout=5

    def setUp(self):
        self.pass_test=True
        """ Nothing to setup """

    def tearDown(self):
        """ Nothing to finish """

    def test_shebang(self):
        with open(self.script_name) as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None))

    def test_lower_case(self):
        letra = random.choice(string.ascii_lowercase)
        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
            self.child.expect('Introduzca una tecla: ', timeout=self.timeout)
            self.child.sendline(letra)
            self.child.expect('{} es una letra'.format(letra), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test)

        self.child.terminate(force=True)

    def test_upper_case(self):
        letra = random.choice(string.ascii_uppercase)
        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
            self.child.expect('Introduzca una tecla: ')
            self.child.sendline(letra)
            self.child.expect('{} es una letra'.format(letra), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test)

        self.child.terminate(force=True)

    def test_digit(self):
        digit = random.choice(string.digits)
        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
            self.child.expect('Introduzca una tecla: ', timeout=self.timeout)
            self.child.sendline(digit)
            self.child.expect('{} es un numero'.format(digit), timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test)

        self.child.terminate(force=True)

    def test_special_char(self):
        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
            self.child.expect('Introduzca una tecla: ', timeout=self.timeout)
            self.child.sendline('\t')
            # I think the output depends on the terminal, so we use a wildcard
            self.child.expect('.* es un caracter especial', timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test)

        self.child.terminate(force=True)

if __name__ == "__main__":
    unittest.main()
