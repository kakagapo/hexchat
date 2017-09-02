#!/usr/bin/env python3

import sys
import cffi

builder = cffi.FFI()

# exports.h
with open(sys.argv[1]) as f:
    builder.embedding_api(f.read())

# imports.h
with open(sys.argv[2]) as f:
    builder.cdef(f.read())

# init.c
with open(sys.argv[3]) as f:
    builder.set_source('_hexchat_embedded', f.read())

# init.py
with open(sys.argv[4]) as f:
    builder.embedding_init_code(f.read())

# python.c
builder.emit_c_code(sys.argv[5])
