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


import hashlib
import os
import glob


def file_hash(file, hasher=None):
    if not hasher:
        hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()


def print_files_tree_with_hashes(root, hasher=None):
    for address, dirs, files in os.walk(root):
        for filename in files:
            path = os.path.join(address, filename)
            print('{} {}'.format(path, file_hash(path, hasher)))


def print_file(filepath):
    file = open(filepath, 'r')
    for line in file:
        print(line)


def print_file_by_mask_list(root, masks: [str]):
    for address, dirs, files in os.walk(root):
        for filename in files:
            path = os.path.join(address, filename)
            for mask in masks:
                if path in glob.glob(os.path.join(address, mask)):
                    print('{} :\n'.format(path))
                    print_file(path)
                    print()


def debug(capi):
    if 'closed_api' in capi.input_xml:
        path = os.path.abspath(os.path.join(capi.output_folder, '..'))
        print(path)
        print()
        files = [
            '*.xml',
            'ExampleKeys.h',
            'PersonImpl.*',
            'CMakeLists.txt'
        ]
        print_file_by_mask_list(path, files)
        # print_files_tree_with_hashes(path)
    pass
