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

import os
import argparse
import shutil


def get_next_backup_folder(output_folder):
    backup_number = 0
    backup_exists = True
    while backup_exists:
        backup_number_str = '{0:03}'.format(backup_number)
        current_backup_folder = os.path.join(output_folder, backup_number_str)
        backup_exists = os.path.exists(current_backup_folder)
        backup_number += 1
    return current_backup_folder


def backup_example(input_folder, example_name, base_backup_folder):
    base_example_library_folder = os.path.join(input_folder, 'examples', example_name, 'library')
    example_include_folder = os.path.join(base_example_library_folder, 'include')
    backup_include_folder = os.path.join(base_backup_folder, example_name, 'include')
    shutil.copytree(example_include_folder, backup_include_folder)
    example_snippets_folder = os.path.join(base_example_library_folder, 'source', 'snippets')
    backup_snippets_folder = os.path.join(base_backup_folder, example_name, 'snippets')
    if os.path.exists(example_snippets_folder):
        shutil.copytree(example_snippets_folder, backup_snippets_folder)
    auto_gen_wrap_cpp = os.path.join(base_example_library_folder, 'source', 'AutoGenWrap.cpp')
    if os.path.exists(auto_gen_wrap_cpp):
        auto_gen_wrap_cpp_destination = os.path.join(base_backup_folder, example_name, 'AutoGenWrap.cpp')
        shutil.copy(auto_gen_wrap_cpp, auto_gen_wrap_cpp_destination)
    else:
        auto_gen_wrap_cpp = os.path.join(base_example_library_folder, 'source', 'auto_gen_wrap.cpp')
        auto_gen_wrap_cpp_destination = os.path.join(base_backup_folder, example_name, 'auto_gen_wrap.cpp')
        shutil.copy(auto_gen_wrap_cpp, auto_gen_wrap_cpp_destination)


def backup_beautiful_capi(input_folder, output_folder):
    print('input folder: {0}'.format(input_folder))
    base_backup_folder = get_next_backup_folder(output_folder)
    print('output folder: {0}'.format(base_backup_folder))
    backup_example(input_folder, 'boost_shared_ptr', base_backup_folder)
    backup_example(input_folder, 'callback', base_backup_folder)
    backup_example(input_folder, 'circular_reference', base_backup_folder)
    backup_example(input_folder, 'copy_semantic', base_backup_folder)
    backup_example(input_folder, 'custom_suffix', base_backup_folder)
    backup_example(input_folder, 'down_cast', base_backup_folder)
    backup_example(input_folder, 'exception', base_backup_folder)
    backup_example(input_folder, 'hello_world', base_backup_folder)
    backup_example(input_folder, 'object_parameter', base_backup_folder)
    backup_example(input_folder, 'point_set', base_backup_folder)
    backup_example(input_folder, 'raw_pointer_semantic', base_backup_folder)
    backup_example(input_folder, 'reference_counted', base_backup_folder)
    backup_example(input_folder, 'single_file', base_backup_folder)
    backup_example(input_folder, 'virtual_interface', base_backup_folder)


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi Backup Copy',
        description='This program backups generated C and C++ files by Beautiful Capi.')

    parser.add_argument(
        '-i', '--input-folder', nargs=None,
        help='specifies input BCapi root folder')
    parser.add_argument(
        '-o', '--output-folder', nargs=None,
        help='specifies output folder for backup files')

    args = parser.parse_args()
    backup_beautiful_capi(args.input_folder, args.output_folder)


if __name__ == '__main__':
    main()
