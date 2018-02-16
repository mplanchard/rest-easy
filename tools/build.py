#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build a distribution."""

from click import command, option
from os import chdir
from pathlib import Path
from shutil import rmtree
from subprocess import Popen


METADATA_PATH = Path(__file__).parent / 'build_metadata'
DEV_VER_PATH = METADATA_PATH / 'version_dev'
RC_VER_PATH = METADATA_PATH / 'version_rc'


def ver_from_file(path):
    """Get a version from a file.

    The version file should just be a textfile with an integer number
    and nothing else.
    """
    with path.open() as ver_file:
        return int(ver_file.read().strip())


def ver_to_file(path, ver):
    """Write a version to a file."""
    with path.open('w') as ver_file:
        ver_file.write('{}\n'.format(ver))


def clean_workspace():
    """Destroy previous build information (but not dists)."""
    build_dir = Path(__file__).parent.parent/'build'
    if build_dir.exists():
        rmtree(build_dir)
    for child in Path(__file__).parent.parent.iterdir():
        if child.is_dir() and str(child).endswith('.egg-info'):
            rmtree(child)


def dev_version():
    """Retrieve the dev version."""
    return ver_from_file(DEV_VER_PATH)


def rc_version():
    """Retrieve the RC version."""
    return ver_from_file(RC_VER_PATH)


def make_build(*extra_cmd_args):
    """Trigger a build."""
    chdir(Path(__file__).parent.parent)
    cmd = ['python', 'setup.py', 'sdist']
    cmd.extend(extra_cmd_args)
    Popen(cmd)
    cmd = ['python', 'setup.py', 'bdist_wheel']
    cmd.extend(extra_cmd_args)
    Popen(cmd)


def make_dev_build(inc):
    """Make a dev build!"""
    ver = dev_version()
    if inc:
        ver += 1
    make_build('egg_info', '--tag-build=dev{}'.format(ver))
    ver_to_file(DEV_VER_PATH, ver)


def make_rc_build(inc):
    """Make an RC build."""
    ver = dev_version()
    if inc:
        ver += 1
    make_build('egg_info', '--tag-build=rc{}'.format(ver))
    ver_to_file(RC_VER_PATH, ver)


def make_prod_build():
    """Make a production build."""
    make_build()


@command()
@option('--dev', 'channel', flag_value='dev', default=True,
        help='Make a dev build')
@option('--rc', 'channel', flag_value='rc', help='Make an RC build')
@option('--prod', 'channel', flag_value='prod', help='Make a production build')
@option('--inc/--no-inc', default=True,
        help='Increment the dev or RC build number')
def main(channel, inc):
    """Make a build."""
    clean_workspace()
    globals()['make_{}_build'.format(channel)](inc)


if __name__ == '__main__':
    main()  # pylint: disable=E1120
