import sys
import importlib
from contextlib import contextmanager
from _hexchat_embedded import ffi, lib

ph = None
hexchat = None
local_interp = None
hexchat_stdout = None
plugins = set()


class Stdout:
    def __init__(self, ph):
        self.ph = ph

    def write(self, string):
        # TODO: This should be buffering until newlines
        lib.hexchat_print(self.ph, string.encode().rstrip(b'\n'))


class Plugin:
    def __init__(self):
        self.ph = None
        self.name = ''
        self.filename = ''
        self.hooks = set()
        self.globals = {}
        self.locals = {}

    @contextmanager
    def hexchat_stdout(self):
        sys.stdout = hexchat_stdout
        sys.stderr = hexchat_stdout
        yield
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def execute(self, string):
        if 'hexchat' not in self.globals:
            self.globals['hexchat'] = hexchat

        with self.hexchat_stdout():
            try:
                exec(string, self.globals, self.locals)
            except Exception as e:
                print(e)

    def loadfile(self, filename):
        with self.hexchat_stdout():
            try:
                self.filename = filename
                with open(filename) as f:
                    data = f.read()
                compiled = compile(data, filename, 'exec', optimize=2)
                exec(compiled, self.globals)

                self.name = self.globals['__module_name__']
                version = self.globals['__module_version__']
                description = self.globals['__module_description__']
                self.ph = lib.hexchat_plugingui_add(ph, filename.encode(), self.name.encode(),
                                                    description.encode(), version.encode(),
                                                    ffi.NULL)
            except Exception as e:
                print(e)
                return False
        return True

    def __del__(self):
        # TODO: Hooks
        if self.ph is not None:
            lib.hexchat_plugingui_remove(ph, self.ph)


@ffi.def_extern()
def on_command(word, word_eol, userdata):
    subcmd = ffi.string(word[2]).decode()

    if subcmd == 'exec':
        python = ffi.string(word_eol[3]).decode()
        if python:
            local_interp.execute(python)

    elif subcmd == 'load':
        filename = ffi.string(word[3]).decode()
        if filename and not any(plugin.filename == filename for plugin in plugins):
            plugin = Plugin()
            if plugin.loadfile(filename):
                plugins.add(plugin)

    elif subcmd == 'unload':
        name = ffi.string(word[3]).decode()
        if name:
            for plugin in plugins:
                if name in (plugin.name, plugin.filename):
                    plugins.remove(plugin)
                    break

    return hexchat.EAT_ALL


@ffi.def_extern()
def plugin_init(plugin_handle):
    global ph
    global local_interp
    global hexchat
    global hexchat_stdout

    ph = plugin_handle
    hexchat_stdout = Stdout(ph)
    libdir = ffi.string(lib.hexchat_get_info(ph, b'libdirfs')).decode()
    sys.path.append(libdir)
    hexchat = importlib.import_module('hexchat')
    hexchat.__dict__['__ph'] = ph
    local_interp = Plugin()

    lib.hexchat_hook_command(ph, b'PY', hexchat.PRI_NORM, lib.on_command, ffi.NULL, ffi.NULL)
    return True


@ffi.def_extern()
def plugin_deinit():
    global plugins
    plugins = set()
    return True
