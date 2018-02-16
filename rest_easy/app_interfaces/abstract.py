# -*- coding: utf-8 -*-
"""Abstract interface for application interfaces.

Interface plugin classes  MUST inherit from this class and implement
required methods.
"""

from abc import ABCMeta
from six import with_metaclass


class AbstractInterface(with_metaclass(ABCMeta)):
    pass
