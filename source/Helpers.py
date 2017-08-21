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


def fix_name(name: str) -> str:
    return name.replace('<', '_').replace('>', '').replace('::', '_').\
        replace('*', 'p').replace(' ', '').replace(',', '_').replace('-', '')


def remove_double_underscore(text: str) -> str:
    while text.find('__') != -1:
        text = text.replace('__', '_')
    return text


def replace_double_greater(template_name):
    while template_name.find('>>') != -1:
        template_name = template_name.replace('>>', '> >')
    return template_name


def get_c_name(name: str) -> str:
    fixed_name = fix_name(name)
    stl_name = pascal_to_stl(fixed_name)
    return remove_double_underscore(stl_name)


def pascal_to_stl(pascal_name: str) -> str:
    result = ''
    first = True
    previous_symbol_is_upper_case = False
    for letter in pascal_name:
        if first:
            result += letter.lower()
            first = False
        else:
            if letter.isupper() and not previous_symbol_is_upper_case:
                result += '_' + letter.lower()
            else:
                result += letter.lower()
        previous_symbol_is_upper_case = letter.isupper() or letter.isdigit()
    return result


def format_type(type_name):
    return replace_double_greater(type_name)


def bool_to_str(value: bool) -> str:
    return 'true' if value else 'false'


def replace_template_to_filename(template_name):
    fixed_name = template_name.replace('<', '').replace('>', '').replace('::', '').replace('*', 'p').replace(' ', '')
    return remove_double_underscore(fixed_name.replace(',', '_'))


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


def if_required_then_add_empty_line(first_flag: bool, out) -> bool:
    if not first_flag:
        out.put_line('')
    return False


def include_headers(out, headers):
    for header in headers:
        out.include_header(header.file, header.system)


def get_full_method_name(method) -> [str]:
    compound_name = [method.name]
    if hasattr(method, 'const') and method.const:
        compound_name.append('const')
    if method.overload_suffix:
        compound_name.append(method.overload_suffix)
    return compound_name


class BeautifulCapiException(Exception):
    def __init__(self, message):
        self.message = message
