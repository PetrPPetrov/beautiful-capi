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
import posixpath
import FileGenerator
from TraitsBase import TraitsBase


class FileTraitsBase(TraitsBase):
    def __init__(self, capi_generator):
        super().__init__(None, capi_generator)


class SingleFile(FileTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)
        self.file_name = os.path.join(self.capi_generator.output_folder,
                                      self.capi_generator.params_description.m_single_header_name)
        self.output_file = FileGenerator.FileGenerator(self.file_name)

    def get_file_for_namespace(self, namespace_path):
        return self.output_file

    def get_file_for_class(self, namespace_path, cur_class):
        return self.output_file


class PosixJoin(object):
    def join(self, path_a, path_b):
         return posixpath.join('/'.join(path_a, path_b))

    def join_to_base(self):
        return ''


class OsJoin(object):
    def __init__(self, base_path):
        self.base_path = base_path

    def join(self, path_a, path_b):
         return os.path.join('/'.join(path_a, path_b))

    def get_base_path(self):
        return self.base_path

class MultipleFiles(FileTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)
        self.base_path = self.capi_generator.output_folder
        self.file2generator = {}

    @staticmethod
    def __posix_join(path_a, path_b):
         return posixpath.join('/'.join(path_a, path_b))

    @staticmethod
    def __os_join(path_a, path_b):
        return os.path.join(path_a, path_b)

    def __get_file_name_base_for_namespace_common(self, namespace_path, join_functor):
        if self.capi_generator.params_description.m_folder_per_namespace:
            result_folder = join_functor.join(self.base_path, namespace_path)
        else:
            result_folder = self.base_path
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        return result_folder

    def __get_file_name_base_for_namespace(self, namespace_path, join_function):
        if self.capi_generator.params_description.m_namespace_header_at_parent_folder:
            return self.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_function)
        else:
            return self.__get_file_name_base_for_namespace_common(namespace_path, join_function)

    def __get_file_name_for_namespace(self, namespace_path, join_function):
        return join_function(
            self.__get_file_name_base_for_namespace(namespace_path, join_function),
            namespace_path[-1] + '.h'
        )

    def __get_file_name_for_class(self, namespace_path, cur_class, join_function):
        if self.capi_generator.params_description.m_file_per_class:
            return join_function(
                self.__get_file_name_base_for_namespace_common(namespace_path, join_function),
                cur_class.m_name + '.h'
            )
        else:
            return self.__get_file_name_for_namespace(namespace_path, join_function)

    def __get_cached_generator(self, file_name):
        if file_name in self.file2generator:
            return self.file2generator[file_name]
        else:
            output_file = FileGenerator.FileGenerator(file_name)
            self.file2generator.update({file_name: output_file})
            return output_file

    def get_file_for_namespace(self, namespace_path):
        output_file_name = self.__get_file_name_for_namespace(namespace_path)
        return self.__get_cached_generator(output_file_name)

    def get_file_for_class(self, namespace_path, cur_class):
        output_file_name = self.__get_file_name_for_class(namespace_path, cur_class)
        return self.__get_cached_generator(output_file_name)

    def include_class_header(self, namespace_path, cur_class):
        if self.capi_generator.params_description.m_file_per_class:



def create_file_traits(capi_generator):
    if capi_generator.params_description.m_generate_single_file:
        return SingleFile(capi_generator)
    else:
        return MultipleFiles(capi_generator)
