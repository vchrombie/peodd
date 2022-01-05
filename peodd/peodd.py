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


"""Script to export the pyproject.toml dev-dependencies to a txt file."""

import os
import re

import click
import tomli
from release_tools.project import Project
from release_tools.repo import RepositoryError
from release_tools.semverup import find_pyproject_file

VERSION_NUMBER_REGEX = r"\d+(?:\.\d+)+"


def write_package_version_to_file(fp, k, v):
    version = re.findall(VERSION_NUMBER_REGEX, v)[0]

    if '^' in v or '>=' in v:
        fp.write("{}>={}\n".format(k, version))
        click.echo("{}>={} ...".format(k, version), nl=False)
    elif v == version:
        fp.write("{}=={}\n".format(k, version))
        click.echo("{}=={} ...".format(k, version), nl=False)
    else:
        msg = "Wrong version number"
        raise click.ClickException(msg)

    click.echo("done")


@click.command()
@click.option('-o', '--output',
              required=True,
              help="Output filename for the dependencies")
@click.option('--non-dev',
              default=False,
              show_default=True,
              is_flag=True,
              help="Export non-dev dependencies")
def main(output, non_dev):
    """Script to export the pyproject.toml dev-dependencies to a txt file."""
    try:
        project = Project(os.getcwd())
    except RepositoryError as e:
        raise click.ClickException(e)

    # Get the pyproject file
    pyproject_file = find_pyproject_file(project)

    with open(pyproject_file, encoding="utf-8") as f:
        try:
            toml_dict = tomli.load(f)
        except tomli.TOMLDecodeError:
            msg = "{} file is not valid".format(pyproject_file)
            raise click.ClickException(msg)

    if non_dev:
        dependencies = toml_dict["tool"]["poetry"]["dependencies"]
        click.echo("Collected dependencies ...", nl=False)
    else:
        dependencies = toml_dict["tool"]["poetry"]["dev-dependencies"]
        click.echo("Collected dev-dependencies ...", nl=False)

    click.echo("done")

    with open(output, "w") as fp:
        for k, v in dependencies.items():
            if type(v) is dict:
                try:
                    v = v['version']
                except KeyError:
                    msg = "Format not supported"
                    # You can open an issue at https://github.com/vchrombie/peodd
                    # for reporting this and more discussion
                    raise click.ClickException(msg)

            write_package_version_to_file(fp, k, v)

    click.echo("Export complete")


if __name__ == '__main__':
    main()
