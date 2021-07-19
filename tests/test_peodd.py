#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CHAOSS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Venu Vardhan Reddy Tekula <venu@chaoss.community>
#


import os
import unittest
import unittest.mock

import click.testing

from peodd._version import __version__
from peodd import peodd


DEV_DEPENDENCIES_CONTENT_PYPROJECT_TOML = """[tool.poetry.dev-dependencies]
foo = "^1.2.1"
bar = ">=1.2.2"
baz = "1.2.3"
"""

DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT = (
    "foo>=1.2.1\nbar>=1.2.2\nbaz==1.2.3\n"
)


class TestPeodd(unittest.TestCase):

    @staticmethod
    def setup_pyproject_file(filepath):
        """Set up some dev-dependencies in the pyproject file"""

        with open(filepath, mode='w') as fd:
            fd.write(DEV_DEPENDENCIES_CONTENT_PYPROJECT_TOML)

    @unittest.mock.patch('peodd.peodd.Project')
    def test_peodd_script(self, mock_project):
        """
        Check if the dev-dependencies of the pyproject.toml format are
        properly converted to the requirements.txt format
        """

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:
            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file)

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])
            self.assertEqual(result.exit_code, 0)

            filepath = os.path.join(fs, 'requirements-dev.txt')
            with open(filepath, 'r') as fd:
                text = fd.read()

            self.assertEqual(text,
                             DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT)

    def test_version(self):
        self.assertRegex(__version__, peodd.VERSION_NUMBER_REGEX)


if __name__ == '__main__':
    unittest.main()
