# -*- coding: utf-8 -*-
"""Test the app_interfaces.util module."""

import pytest

from rest_easy.app_interfaces import util


class TestGetDistname:

    @staticmethod
    def new_inst(base):

        class Foo(base):
            pass

        return Foo()

    @staticmethod
    def available_names():
        return 'flask', 'django'

    class BaseOne:
        __module__ = 'flask.app'

    class BaseTwo:
        __module__ = 'django.apps'

    class BaseThree(BaseOne):
        __module__ = 'foo.bar'

    @pytest.mark.parametrize('base, exp', (
        (BaseOne, 'flask'),
        (BaseTwo, 'django'),
        (BaseThree, 'flask'),
    ))
    def test_get_distname_available(self, base, exp):
        """Ensure we can grab the dist name from a class."""
        inst = self.new_inst(base)
        assert exp == util.get_distname(inst, self.available_names())

    @pytest.mark.parametrize('base, exp', (
        (BaseOne, 'flask'),
        (BaseTwo, 'django'),
        (BaseThree, 'flask'),
    ))
    def test_get_distname_not_available(self, base, exp):
        inst = self.new_inst(base)
        with pytest.raises(TypeError):
            util.get_distname(inst, ())

