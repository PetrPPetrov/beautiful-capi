#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2015 Petr Petrovich Petrov
#
# This file is part of Beautiful Capi.
#
# Beautiful Capi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Beautiful Capi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
#


from Parser import TConstructor
from Parser import TCodeBlock
from Parser import TCodeLine


def pascal_to_stl(pascal_name):
    return ''.join(['_' + symbol.lower() if symbol.isupper() else symbol for symbol in pascal_name])


def get_self(cur_class):
    if cur_class.pointer_access:
        return '(*self)'
    else:
        return 'self'


def put_raw_pointer_structure(output_file):
    output_file.put_line('struct raw_pointer_holder { void* raw_pointer; };')


def get_return_copy_or_add_ref_default_value(constructor_or_method):
    if type(constructor_or_method) is TConstructor:
        return False
    else:
        return True


def get_return_copy_or_add_ref(constructor_or_method):
    if constructor_or_method.return_copy_or_add_ref_filled:
        return constructor_or_method.return_copy_or_add_ref
    else:
        return get_return_copy_or_add_ref_default_value(constructor_or_method)


def save_file_generator_to_code_blocks(file_generator, code_blocks):
    new_code_block = TCodeBlock()
    for cur_line in file_generator.get_lines():
        new_line = TCodeLine()
        new_line.text = cur_line.replace('\n', '')
        new_code_block.lines.append(new_line)
    code_blocks.append(new_code_block)


def save_line_as_new_code_block(text, code_blocks):
    new_code_block = TCodeBlock()
    new_line = TCodeLine()
    new_line.text = text
    new_code_block.lines.append(new_line)
    code_blocks.append(new_code_block)


def output_code_blocks(output_file, code_blocks, prepend_empty_line=False):
    if prepend_empty_line and code_blocks:
        output_file.put_line('')
    for cur_code_block in code_blocks:
        for cur_code_line in cur_code_block.lines:
            output_file.put_line(cur_code_line.text)
    if not prepend_empty_line and code_blocks:
        output_file.put_line('')


class NamespaceScope(object):
    def __init__(self, cur_namespace_path, cur_namespace):
        self.cur_namespace_path = cur_namespace_path
        self.cur_namespace = cur_namespace

    def __enter__(self):
        self.cur_namespace_path.append(self.cur_namespace.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur_namespace_path.pop()
