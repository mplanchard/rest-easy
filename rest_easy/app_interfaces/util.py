# -*- coding: utf-8 -*-
"""Utilities for application interfaces."""

from pkg_resources import iter_entry_points


def get_distname(app, available_names):
    """Attempt to get the root distname of the app.

    :param app: an application instance
    :returns: the root of the application's class' module name
    :rtype: str
    """
    for kls in app.__class__.__mro__:
        distname = kls.__module__.split('.')[0]
        if distname in available_names:
            return distname
    raise TypeError(
        '{} does not appear to be an application instance from one of the '
        'configured libraries. Support for more libraries can be added via'
        'rest-easy plugins. Currently available libraries are: {}'.format(
            app, available_names
        )
    )


def interface_plugins():
    """Return interface plugins currently configured."""
    return {
        ep.name: ep for ep in iter_entry_points('rest_easy.app_interfaces')
    }
