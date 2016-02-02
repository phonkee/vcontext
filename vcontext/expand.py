"""
expand support for Context
"""

import inspect

import functools

__plugins__ = []


def register(plugin):
    """
    Register plugin, can be used also as decorator
    :param plugin:
    :return:
    """
    assert inspect.isclass(plugin) and issubclass(plugin, Plugin), \
        'register_plugin accepts only subclass of Plugin'

    print 'registering'
    __plugins__.append(plugin)

    return functools.wraps(plugin)


def apply(context):
    """
    apply context
    :param context:
    :return:
    """
    pass


class Plugin(object):
    """
    Plugin object
    """

    @classmethod
    def process(cls, keys):
        pass
