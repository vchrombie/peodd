#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CHAOSS
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
#     Lewi Uberg <lewi@uberg.me>
#


import os
import unittest
import unittest.mock

import click.testing
from peodd import peodd
from peodd._version import __version__
from release_tools.repo import RepositoryError

DEPENDENCIES_CONTENT_PYPROJECT_TOML = """
[tool.poetry.dependencies]
foo1 = "^1.2.3"
bar1 = ">=1.2.3"
bas1 = {extras = ["bar1"], version = "^1.2.3"}
baz1 = "1.2.3"

[tool.poetry.dev-dependencies]
foo2 = "^1.2.3"
bar2 = ">=1.2.3"
bas2 = {extras = ["bar2"], version = "^1.2.3"}
baz2 = "1.2.3"
"""

INVALID_CONTENT_PYPROJECT_TOML = """
[tool.poetry.dev-dependencies
foo = "^1.2.1"
bar = ">=1.2.2"
baz = "1.2.3"
"""

INVALID_VERSION_NUMBER_CONTENT = """
[tool.poetry.dev-dependencies]
foo = "^1.2.1"
bar = "+1.2.2"
baz = "1.2.3"
"""

GIT_URL_DEPENDENCY_CONTENT = """
[tool.poetry.dev-dependencies]
foo = "^1.2.1"
bar = {git = "https://github.com/foobarbaz/bar.git", rev = "master"}
baz = "1.2.3"
"""

NON_DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT = (
    "foo1>=1.2.3\nbar1>=1.2.3\nbas1>=1.2.3\nbaz1==1.2.3\n"
)

DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT = (
    "foo2>=1.2.3\nbar2>=1.2.3\nbas2>=1.2.3\nbaz2==1.2.3\n"
)

MOCK_REPOSITORY_ERROR = (
    "Error: "
)

INVALID_PYPROJECT_TOML_ERROR = (
    "Error: {}/pyproject.toml file is not valid"
)

INVALID_VERSION_NUMBER_ERROR = (
    "Error: Wrong version number"
)

INVALID_DEPENDENCY_FORMAT_ERROR = (
    "Error: Format not supported"
)


class TestPeodd(unittest.TestCase):

    @staticmethod
    def setup_pyproject_file(filepath, content):
        """Set up some dev-dependencies in the pyproject file"""

        with open(filepath, mode='w') as fd:
            fd.write(content)

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
            self.setup_pyproject_file(project_file, DEPENDENCIES_CONTENT_PYPROJECT_TOML)

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])
            self.assertEqual(result.exit_code, 0)

            filepath = os.path.join(fs, 'requirements-dev.txt')
            with open(filepath, 'r') as fd:
                text = fd.read()

            self.assertEqual(text, DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT)

    @unittest.mock.patch('peodd.peodd.Project')
    def test_peodd_script_non_dev(self, mock_project):
        """
        Check if the main dependencies of the pyproject.toml format are
        properly converted to the requirements.txt format. Also check if
        the default output file name is used.
        """

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:
            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file, DEPENDENCIES_CONTENT_PYPROJECT_TOML)

            # Run the script command
            result = runner.invoke(peodd.main, ['--non-dev', '-o', 'requirements.txt'])
            self.assertEqual(result.exit_code, 0)

            filepath = os.path.join(fs, 'requirements.txt')
            with open(filepath, 'r') as fd:
                text = fd.read()

            self.assertEqual(text, NON_DEV_DEPENDENCIES_CONTENT_REQUIREMENTS_TXT)

    @unittest.mock.patch('peodd.peodd.Project')
    def test_repository_error(self, mock_project):
        """Check if it stops working when it encounters RepositoryError exception"""

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:

            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file, DEPENDENCIES_CONTENT_PYPROJECT_TOML)

            mock_project.side_effect = RepositoryError()

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])

            self.assertEqual(result.exit_code, 1)

            lines = result.stderr.split('\n')
            self.assertEqual(lines[-2], MOCK_REPOSITORY_ERROR)

            filepath = os.path.join(fs, 'requirements-dev.txt')
            self.assertEqual(os.path.exists(filepath), False)

    @unittest.mock.patch('peodd.peodd.Project')
    def test_invalid_pyproject_toml(self, mock_project):
        """Check if it stops working for an invalid pyproject.toml file"""

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:
            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file, INVALID_CONTENT_PYPROJECT_TOML)

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])
            self.assertEqual(result.exit_code, 1)

            lines = result.stderr.split('\n')
            self.assertEqual(lines[-2], INVALID_PYPROJECT_TOML_ERROR.format(fs))

            filepath = os.path.join(fs, 'requirements-dev.txt')
            self.assertEqual(os.path.exists(filepath), False)

    @unittest.mock.patch('peodd.peodd.Project')
    def test_invalid_version_number(self, mock_project):
        """Check if it stops working for an invalid version number for dev-dependencies"""

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:
            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file, INVALID_VERSION_NUMBER_CONTENT)

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])
            self.assertEqual(result.exit_code, 1)

            self.assertRaises(Exception)

            lines = result.stderr.split('\n')
            self.assertEqual(lines[-2], INVALID_VERSION_NUMBER_ERROR.format(fs))

    @unittest.mock.patch('peodd.peodd.Project')
    def test_git_url_dependency(self, mock_project):
        """Check if it skips the git url dependecny"""

        runner = click.testing.CliRunner(mix_stderr=False)

        with runner.isolated_filesystem() as fs:
            project_file = os.path.join(fs, "pyproject.toml")
            mock_project.return_value.pyproject_file = project_file
            self.setup_pyproject_file(project_file, GIT_URL_DEPENDENCY_CONTENT)

            # Run the script command
            result = runner.invoke(peodd.main, ['-o', 'requirements-dev.txt'])
            self.assertEqual(result.exit_code, 1)

            self.assertRaises(Exception)

            lines = result.stderr.split('\n')
            self.assertEqual(lines[-2], INVALID_DEPENDENCY_FORMAT_ERROR.format(fs))

    def test_version(self):
        self.assertRegex(__version__, peodd.VERSION_NUMBER_REGEX)


if __name__ == '__main__':
    unittest.main()
