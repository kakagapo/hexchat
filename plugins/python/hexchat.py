from functools import wraps
from _hexchat_embedded import ffi, lib

__doc__ = 'HexChat Scripting Interface'
__version__ = (1, 0)

EAT_ALL = 0
EAT_HEXCHAT = 1
EAT_XCHAT = EAT_HEXCHAT
EAT_PLUGIN = 2
EAT_ALL = EAT_HEXCHAT | EAT_PLUGIN

PRI_LOWEST = -128
PRI_LOW = -64
PRI_NORM = 0
PRI_HIGH = 64
PRI_HIGHEST = 127


# This just mimics the behavior of the CPython API
def __signature(*types):
    def check_signature(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if len(args) < len(types):
                raise TypeError('{}() takes at least {} argument(s) ({} given)'.format(
                                f.__name__, len(types), len(args)))
            for (arg, type_) in zip(args, types):
                if not isinstance(arg, type_):
                    raise TypeError('An {} is required (got type {})'.format(type_, type(arg)))
            return f(*args, **kwargs)
        return wrapper
    return check_signature


@__signature(str)
def command(command):
    lib.hexchat_command(__ph, command.encode())


@__signature(int, callable)  # TODO: userdata
def hook_timer(timeout, callback):
    # We need a reference to the plugin class here.
    return lib.hexchat_hook_timer(__ph, timeout, lib.on_timer, ffi.NULL)


@__signature(int)
def unhook(handle):
    return lib.hexchat_unhook(__ph, handle)
