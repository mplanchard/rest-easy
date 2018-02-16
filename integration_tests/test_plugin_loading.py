# -*- coding: utf-8 -*-
"""Validate that our plugin mocks are not unreasonable.

We expect that the application interfaces we provide in ``app_interfaces``
will have entry points registered in ``setup.py``. Here, we do a fresh
install and verify that what we expect to be loaded is, in fact, loaded.
"""

import json
from os import chdir
from pathlib import Path
from subprocess import PIPE, Popen, check_call
from sys import version_info
from tempfile import TemporaryDirectory

import pytest

PKG_DIR = Path(__file__).parent.parent
PY2 = version_info[0] == 2


class TestInterfacePlugins:

    def test_local_plugins_available(self):
        exp_plugins = ['flask']
        with TemporaryDirectory() as tmpdir:
            venv_dir = Path(tmpdir) / 'venv'
            chdir(tmpdir)
            if PY2:
                check_call(['virtualenv', '-p', 'python2', str(venv_dir)])
            else:
                check_call(['python', '-m', 'venv', str(venv_dir)])
            pip = str(venv_dir/'bin'/'pip')
            python = str(venv_dir/'bin'/'python')
            check_call([pip, 'install', 'ipdb'])
            check_call([pip, 'install', '--no-cache-dir', str(PKG_DIR)])
            cmd = (
                '{} -c '
                '"from rest_easy.app_interfaces import util; '
                'import json; '
                'print(json.dumps(list(util.interface_plugins())))"'.format(
                    python
                )
            )
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
        plugins = json.loads(out)
        assert exp_plugins == plugins, 'out: {}, err: {}'.format(out, err)
