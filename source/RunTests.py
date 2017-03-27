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
import subprocess
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
        auto_gen_wrap_cpp_destination = os.path.join(base_backup_folder, example_name, 'AGenWrap.cpp')
        shutil.copy(auto_gen_wrap_cpp, auto_gen_wrap_cpp_destination)
    else:
        auto_gen_wrap_cpp = os.path.join(base_example_library_folder, 'source', 'auto_gen_wrap.cpp')
        auto_gen_wrap_cpp_destination = os.path.join(base_backup_folder, example_name, 'agen_wrap.cpp')
        shutil.copy(auto_gen_wrap_cpp, auto_gen_wrap_cpp_destination)


def backup_test(input_folder, test_family, test_name, base_backup_folder):
    base_test_library_folder = os.path.join(input_folder, 'tests', test_family, 'library')
    test_include_folder = os.path.join(base_test_library_folder, 'include', test_name)
    backup_include_folder = os.path.join(base_backup_folder, test_family, test_name, 'include')
    shutil.copytree(test_include_folder, backup_include_folder)
    test_snippets_folder = os.path.join(base_test_library_folder, 'source', 'snippets_' + test_name)
    backup_snippets_folder = os.path.join(base_backup_folder, test_family, test_name, 'snippets')
    if os.path.exists(test_snippets_folder):
        shutil.copytree(test_snippets_folder, backup_snippets_folder)
    auto_gen_wrap_cpp = os.path.join(base_test_library_folder, 'source', 'AutoGenWrap_{0}.cpp'.format(test_name))
    auto_gen_wrap_cpp_destination = os.path.join(base_backup_folder, test_family, test_name, 'AGenWrap.cpp')
    shutil.copy(auto_gen_wrap_cpp, auto_gen_wrap_cpp_destination)


def run_example(input_folder, example_name, backup_file):
    bin_folder = os.path.join(input_folder, 'bin')
    os.chdir(bin_folder)

    cs_popen = subprocess.Popen('./' + example_name + '_client', bufsize=-1, shell=False, stdout=subprocess.PIPE)
    std_out, std_error = cs_popen.communicate()
    cs_popen.wait()

    with open(backup_file + '.run', 'wb') as output_file:
        output_file.write(str.encode('{0}\n'.format('./' + example_name + '_client')))
        output_file.write(str.encode('___std::cout___\n'))
        if std_out:
            output_file.write(std_out)
        output_file.write(str.encode('___std::cerr___\n'))
        if std_error:
            output_file.write(std_error)
        output_file.write(str.encode('___eof___\n'))


def process_example(input_folder, example_name, base_backup_folder):
    backup_example(input_folder, example_name, base_backup_folder)
    run_example(input_folder, example_name, os.path.join(base_backup_folder, example_name, example_name))


def process_test(input_folder, test_family, test_name, base_backup_folder):
    backup_test(input_folder, test_family, test_name, base_backup_folder)
    run_example(input_folder, '{0}_{1}'.format(test_family, test_name),
                os.path.join(base_backup_folder, test_family, test_name, test_name))


def run_tests(input_folder, output_folder):
    print('input folder: {0}'.format(input_folder))
    base_backup_folder = get_next_backup_folder(output_folder)
    print('output folder: {0}'.format(base_backup_folder))
    process_example(input_folder, 'boost_shared_ptr', base_backup_folder)
    process_example(input_folder, 'callback', base_backup_folder)
    process_example(input_folder, 'circular_reference', base_backup_folder)
    process_example(input_folder, 'clanguage', base_backup_folder)
    process_example(input_folder, 'class_wrap_name', base_backup_folder)
    process_example(input_folder, 'copy_semantic', base_backup_folder)
    process_example(input_folder, 'custom_suffix', base_backup_folder)
    process_example(input_folder, 'down_cast', base_backup_folder)
    process_example(input_folder, 'exception', base_backup_folder)
    process_example(input_folder, 'hello_world', base_backup_folder)
    process_example(input_folder, 'mapped_types', base_backup_folder)
    process_example(input_folder, 'mixed_semantic', base_backup_folder)
    process_example(input_folder, 'object_parameter', base_backup_folder)
    process_example(input_folder, 'overload_suffix', base_backup_folder)
    process_example(input_folder, 'point_set', base_backup_folder)
    process_example(input_folder, 'raw_pointer_semantic', base_backup_folder)
    process_example(input_folder, 'reference_counted', base_backup_folder)
    process_example(input_folder, 'template', base_backup_folder)
    process_example(input_folder, 'unit_test', base_backup_folder)
    process_example(input_folder, 'virtual_interface', base_backup_folder)
    process_test(input_folder, 'file_options', 'test00', base_backup_folder)
    process_test(input_folder, 'file_options', 'test01', base_backup_folder)


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi Test Runner',
        description='This program runs all executables and backups generated C and C++ files.')

    parser.add_argument(
        '-i', '--input-folder', nargs=None,
        help='specifies input BCapi root folder')
    parser.add_argument(
        '-o', '--output-folder', nargs=None,
        help='specifies output folder for backup files')

    args = parser.parse_args()
    run_tests(args.input_folder, args.output_folder)


if __name__ == '__main__':
    main()
