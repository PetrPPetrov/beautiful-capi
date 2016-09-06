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
from Parser import TLifecycle
from LifecycleTraits import CreateLifecycleTraits


def pascal_to_stl(pascal_name):
    result = ''
    first = True
    for letter in pascal_name:
        if first:
            result += letter.lower()
            first = False
        else:
            if letter.isupper():
                result += '_' + letter.lower()
            else:
                result += letter
    return result


def replace_template_to_filename(template_name):
    return template_name.replace('<', '_').replace('>', '').replace('::', '').replace('*', 'p').replace(' ', '')


def replace_template_to_c_id(template_name):
    return template_name.replace('<', '_').replace('>', '').replace('::', '').replace('*', 'p').replace(' ', '')


def replace_double_greater(template_name):
    while template_name.find('>>') != -1:
        template_name = template_name.replace('>>', '> >')
    return template_name


def get_template_name(type_name):
    if type_name.find('<') == -1:
        return type_name
    else:
        return type_name[:type_name.find('<')]


def get_template_tail(type_name):
    if type_name.find('<') == -1:
        return ''
    else:
        return type_name[type_name.find('<'):]


def get_template_arguments_count(type_name):
    if type_name.find('<') == -1:
        return 0
    level = 0
    index = type_name.find('<')
    arguments_count = 1
    while index < len(type_name):
        if type_name[index] == '<':
            level += 1
        elif type_name[index] == '>':
            level -= 1
        elif level == 1 and type_name[index] == ',':
            arguments_count += 1
        index += 1
    return arguments_count


def get_template_argument(type_name, argument_index):
    if type_name.find('<') == -1:
        return None
    level = 0
    index = type_name.find('<')
    cur_argument_index = 0
    cur_argument_value = ''
    while index < len(type_name):
        if type_name[index] == '>':
            level -= 1
        if level == 1 and type_name[index] == ',':
            if cur_argument_index == argument_index:
                return cur_argument_value.strip()
            cur_argument_index += 1
            cur_argument_value = ''
        elif level > 0:
            cur_argument_value += type_name[index]
        if type_name[index] == '<':
            level += 1
        index += 1
    if cur_argument_index == argument_index:
        return cur_argument_value.strip()
    else:
        return None


def replace_template_argument(type_name, argument_index, new_value):
    if type_name.find('<') == -1:
        return type_name
    level = 0
    index = type_name.find('<')
    cur_argument_index = 0
    cur_argument_start = index + 1
    while index < len(type_name):
        if type_name[index] == '>':
            level -= 1
        if level == 1 and type_name[index] == ',':
            if cur_argument_index == argument_index:
                return (type_name[:cur_argument_start] + new_value + type_name[index:]).strip()
            cur_argument_index += 1
            cur_argument_start = index + 1
        if type_name[index] == '<':
            level += 1
        index += 1
    if cur_argument_index == argument_index:
        return (type_name[:cur_argument_start] + new_value + '>').strip()
    else:
        return None


def format_type(type_name):
    return replace_double_greater(type_name)


def get_self(cur_class):
    if cur_class.pointer_access:
        return '(*self)'
    else:
        return 'self'


def put_raw_pointer_structure(output_file):
    output_file.put_line('struct raw_pointer_holder { void* raw_pointer; };')


def get_return_copy_or_add_ref_default_value(constructor_or_method, class_object):
    if class_object.lifecycle == TLifecycle.copy_semantic:
        return False
    if type(constructor_or_method) is TConstructor:
        return False
    else:
        return True


def get_return_copy_or_add_ref(constructor_or_method, class_object):
    if constructor_or_method.return_copy_or_add_ref_filled:
        return constructor_or_method.return_copy_or_add_ref
    else:
        return get_return_copy_or_add_ref_default_value(constructor_or_method, class_object)


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


class BeautifulCapiException(Exception):
    def __init__(self, message):
        self.message = message

