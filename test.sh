#!/bin/sh
# macabre targets Python, so these bindings cannot be type-checked or tested by
# the stock `gleam` compiler (it does not recognise the python external target).
# Tests for the pure Gleam logic live in test/simplifile_test.gleam and run under
# a macabre test harness. Here we at least syntax-check the Python FFI:
set -e
python3 -m py_compile src/simplifile_bindings.py
echo "ok: simplifile_bindings.py compiles"