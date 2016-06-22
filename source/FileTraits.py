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
        if not os.path.exists(self.capi_generator.output_folder):
            os.makedirs(self.capi_generator.output_folder)
        self.file_name = os.path.join(self.capi_generator.output_folder,
                                      self.capi_generator.params_description.m_single_header_name)
        self.output_file = FileGenerator.FileGenerator(self.file_name)

    def get_file_for_namespace(self, namespace_path):
        return self.output_file

    def get_file_for_class(self, namespace_path, cur_class):
        return self.output_file

    def get_file_for_capi(self, namespace_path):
        return self.output_file

    def get_file_for_fwd(self, namespace_path):
        return self.output_file

    def get_file_for_forward_holder(self):
        return self.output_file

    def get_file_for_check_and_throw_exception(self):
        return self.output_file

    def include_namespace_header(self, namespace_path):
        pass

    def include_class_header(self, namespace_path, cur_class):
        pass

    def include_capi_header(self, namespace_path):
        pass

    def include_fwd_header(self, namespace_path):
        pass

    def include_forward_holder_header(self):
        pass

    def include_check_and_throw_exception_header(self):
        pass


class PosixJoin(object):
    def join(self, path_a, path_b):
        # return posixpath.join('/'.join([path_a, path_b]))
        return posixpath.join(path_a, path_b)

    def join_to_base(self, path):
        result = ''
        for cur_path in path:
            result = posixpath.join(result, cur_path)
        return result

    def get_base_path(self):
        return ''

    def create_if_required(self, path):
        pass


class OsJoin(object):
    def __init__(self, base_path):
        self.base_path = base_path

    def join(self, path_a, path_b):
        return os.path.join(path_a, path_b)

    def join_to_base(self, path):
        result = self.base_path
        for cur_path in path:
            result = os.path.join(result, cur_path)
        return result

    def get_base_path(self):
        return self.base_path

    def create_if_required(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


class MultipleFiles(FileTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)
        self.base_path = self.capi_generator.output_folder
        self.file2generator = {}

    def __get_file_name_base_for_namespace_common(self, namespace_path, join_traits):
        if self.capi_generator.params_description.m_folder_per_namespace:
            result_folder = join_traits.join_to_base(namespace_path)
        else:
            result_folder = join_traits.get_base_path()
        join_traits.create_if_required(result_folder)
        return result_folder

    def __get_file_name_base_for_namespace(self, namespace_path, join_traits):
        if self.capi_generator.params_description.m_namespace_header_at_parent_folder:
            return self.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits)
        else:
            return self.__get_file_name_base_for_namespace_common(namespace_path, join_traits)

    def __get_file_name_for_namespace(self, namespace_path, join_traits):
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path, join_traits),
            namespace_path[-1] + '.h'
        )

    def __get_file_name_for_class(self, namespace_path, cur_class, join_traits):
        if self.capi_generator.params_description.m_file_per_class:
            return join_traits.join(
                self.__get_file_name_base_for_namespace_common(namespace_path, join_traits),
                cur_class.m_name + '.h'
            )
        else:
            return self.__get_file_name_for_namespace(namespace_path, join_traits)

    def __get_file_name_for_capi(self, namespace_path, join_traits):
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path[0:1], join_traits),
            namespace_path[0] + self.capi_generator.params_description.m_capi_header_suffix + '.h'
        )

    def __get_file_name_for_fwd(self, namespace_path, join_traits):
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path[0:1], join_traits),
            namespace_path[0] + self.capi_generator.params_description.m_fwd_header_suffix + '.h'
        )

    def __get_cached_generator(self, file_name):
        if file_name in self.file2generator:
            return self.file2generator[file_name]
        else:
            output_file = FileGenerator.FileGenerator(file_name)
            self.file2generator.update({file_name: output_file})
            return output_file

    def __include_file(self, file_name):
        self.put_line('#include "{0}"'.format(file_name))

    def get_file_for_namespace(self, namespace_path):
        output_file_name = self.__get_file_name_for_namespace(namespace_path, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_class(self, namespace_path, cur_class):
        output_file_name = self.__get_file_name_for_class(namespace_path, cur_class, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_capi(self, namespace_path):
        output_file_name = self.__get_file_name_for_capi(namespace_path, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_fwd(self, namespace_path):
        output_file_name = self.__get_file_name_for_fwd(namespace_path, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_forward_holder(self):
        return self.__get_cached_generator(
            os.path.join(self.base_path, self.capi_generator.params_description.m_forward_holder_filename)
        )

    def get_file_for_check_and_throw_exception(self):
        return self.__get_cached_generator(
            os.path.join(self.base_path, self.capi_generator.params_description.m_check_and_throw_exception_filename)
        )

    def include_namespace_header(self, namespace_path):
        self.__include_file(self.__get_file_name_for_namespace(namespace_path, PosixJoin()))

    def include_class_header(self, namespace_path, cur_class):
        if self.capi_generator.params_description.m_file_per_class:
            self.__include_file(self.__get_file_name_for_class(namespace_path, cur_class, PosixJoin()))

    def include_capi_header(self, namespace_path):
        self.__include_file(self.__get_file_name_for_capi(namespace_path, PosixJoin()))

    def include_fwd_header(self, namespace_path):
        self.__include_file(self.__get_file_name_for_fwd(namespace_path, PosixJoin()))

    def include_forward_holder_header(self):
        self.__include_file(self.capi_generator.params_description.m_forward_holder_filename)

    def include_check_and_throw_exception_header(self):
        self.__include_file(self.capi_generator.params_description.m_check_and_throw_exception_filename)


def create_file_traits(capi_generator):
    if capi_generator.params_description.m_generate_single_file:
        return SingleFile(capi_generator)
    else:
        return MultipleFiles(capi_generator)


class CreateFileTraits(object):
    def __init__(self, capi_generator):
        self.capi_generator = capi_generator
        self.previous_file_traits = capi_generator.file_traits

    def __enter__(self):
        self.capi_generator.file_traits = create_file_traits(self.capi_generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capi_generator.file_traits = self.previous_file_traits
