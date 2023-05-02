#!/usr/bin/env python3

import os
import pexpect
import random
import re
from shutil import rmtree
from stat import S_IXUSR, S_ISREG, S_IEXEC
import string
import sys
from tempfile import mkdtemp
import unittest

class TestPractica2_6(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Find script directory and store its name in a variable """
        cls.my_dir=os.path.dirname(os.path.realpath(__file__))
        cls.script_name=os.path.realpath('{}/../practica_2/practica2_6.sh'.format(cls.my_dir))
        cls.home=os.getenv("HOME")
        cls.timeout=5

    def setUp(self):
        self.pass_test=True

    def tearDown(self):
        """ Nothing to finish """

    def test_shebang(self):
        with open(self.script_name) as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None))

    # helper function
    def is_reg_exe(self, fname):
        """ This function returns true if the file name fname
            is a regular file and can be executed
        """
        st_mode = os.stat(fname).st_mode
        return st_mode & S_IXUSR and S_ISREG(st_mode)

    def find_bin_dir_candidates(self):
        """ Return a list of directories matching the binXXX pattern
        """
        home=self.home
        pattern=re.compile('bin\w\w\w')
        return [ os.path.abspath(home + '/' + d) for d in os.listdir(home) if os.path.isdir(os.path.abspath(home + '/' + d)) and pattern.match(d) ]

    def find_bin_dir(self):
        """ Find the directory bin\w\w\w that is the least frequency modified

            Returns a tuple with a boolean value and a directory name
        """

        candidate_dirs= self.find_bin_dir_candidates()
        # return the least recently modified directory
        if len(candidate_dirs) == 0:
            return True, ""
        else:
            return False, sorted(candidate_dirs, key=lambda d: os.stat(d).st_mtime)[0]

    def test_existing_dir(self):
        """ This test creates the destination directory if it does not exist
        """

        # if there is no bin_dir, we create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        home=self.home

        if bin_dir_required:
            bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            while os.path.isdir(bin_dir):
                bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            # directory creation
            os.mkdir(bin_dir)

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_reg_exe(f) and not f.startswith('.') ]

        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF, timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        dstdir_line=output_lines[0]
        output_lines.pop(0)
        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == dstdir_line, msg='Expected {}, Found: {}'.format(expected_dstdir_line, dstdir_line))

        # Do all matches
        for fname in exec_files:
            self.assertTrue('./{} ha sido copiado a {}'.format(fname, bin_dir) in output_lines, msg='{} not found'.format(fname))

        self.assertTrue('Se han copiado {} archivos'.format(str(len(exec_files))))
        self.assertTrue(len(output_lines) == (len(exec_files)+1))

        self.child.terminate(force=True)

        if bin_dir_required:
            rmtree(bin_dir)

    def test_subdir_no_copy(self):
        """ Create a subdirectory to avoid its copy
        """

        # if there is no bin_dir, we create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        home=self.home

        if bin_dir_required:
            bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            while os.path.isdir(bin_dir):
                bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            # directory creation
            os.mkdir(bin_dir)

        # create a subdirectory in the current directory
        tmp_dir=mkdtemp(prefix=' with spaces ', dir='./')
        # ensure executable mode
        os.chmod(tmp_dir, os.stat(tmp_dir).st_mode | S_IEXEC)

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_reg_exe(f) and not f.startswith('.') ]

        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF, timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        dstdir_line=output_lines[0]
        output_lines.pop(0)
        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == dstdir_line, msg='Expected {}, Found: {}'.format(expected_dstdir_line, dstdir_line))

        # Do all matches
        for fname in exec_files:
            self.assertTrue('./{} ha sido copiado a {}'.format(fname, bin_dir) in output_lines, msg='{} not found'.format(fname))

        self.assertTrue('Se han copiado {} archivos'.format(str(len(exec_files))))
        self.assertTrue(len(output_lines) == (len(exec_files)+1))

        if bin_dir_required:
            rmtree(bin_dir)

        rmtree(tmp_dir)

        self.child.terminate(force=True)

    # @unittest.skip("Activar en curso 2018/2019")
    def test_no_files_to_copy(self):
        """ This test creates a new empty directory and runs the script there
        """

        # if there is no bin_dir, we create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        home=self.home

        if bin_dir_required:
            bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            while os.path.isdir(bin_dir):
                bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            # directory creation
            os.mkdir(bin_dir)

        # create a temporal directory and copy the script there
        tmp_dir=mkdtemp(dir='./')

        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), cwd=tmp_dir, encoding='utf-8')
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF, timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == output_lines[0], msg='Expected: {}, Found: {}'.format(expected_dstdir_line, output_lines[0]))

        expected_ncopied_line = 'No se ha copiado ningun archivo'
        self.assertEqual(expected_ncopied_line, output_lines[1], msg='Expected: {}, Found: {}'.format(expected_ncopied_line, output_lines[1]))

        self.child.terminate(force=True)

        if bin_dir_required:
            rmtree(bin_dir)

        rmtree(tmp_dir)

    def test_dir_creation(self):
        """ This test forces the creation of the destination directory
        """

        for bin_dir in self.find_bin_dir_candidates():
            rmtree(bin_dir)

        # if there is no bin_dir, the script should create one
        bin_dir_required=True

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_reg_exe(f) and not f.startswith('.') ]

        try:
            self.child = pexpect.spawn('/bin/bash "{}"'.format(self.script_name), encoding='utf-8')
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF, timeout=self.timeout)
        except:
            self.pass_test=False
        self.assertTrue(self.pass_test, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        if bin_dir_required:
            fline=output_lines[0]
            output_lines.pop(0) # remove first element list
            self.assertTrue(fline.startswith('Se ha creado el directorio '), msg='Invalid directory creation message')
            bin_dir=os.path.abspath(fline.split(' ')[-1])

        dstdir_line=output_lines[0]
        output_lines.pop(0)
        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == dstdir_line, msg='Expected {}, Found: {}'.format(expected_dstdir_line, dstdir_line))

        # Do all matches
        for fname in exec_files:
            self.assertTrue('./{} ha sido copiado a {}'.format(fname, bin_dir) in output_lines, msg='{} not found'.format(fname))

        self.assertTrue('Se han copiado {} archivos'.format(str(len(exec_files))))
        self.assertTrue(len(output_lines) == (len(exec_files)+1))

        self.child.terminate(force=True)

        if bin_dir_required:
            rmtree(bin_dir)

if __name__ == "__main__":
    unittest.main()
