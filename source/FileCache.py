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

from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator
from Helpers import replace_template_to_filename


class PosixJoin(object):
    @staticmethod
    def join(path_a: str, path_b: str) -> str:
        return posixpath.join(path_a, path_b)

    @staticmethod
    def join_to_base(path: str) -> str:
        result = ''
        for cur_path in path:
            result = posixpath.join(result, cur_path)
        return result

    @staticmethod
    def get_base_path() -> str:
        return ''

    @staticmethod
    def create_if_required(path: str):
        pass


class OsJoin(object):
    def __init__(self, base_path: str):
        self.base_path = base_path

    @staticmethod
    def join(path_a: str, path_b: str) -> str:
        return os.path.join(path_a, path_b)

    def join_to_base(self, path: str) -> str:
        result = self.base_path
        for cur_path in path:
            result = os.path.join(result, cur_path)
        return result

    def get_base_path(self) -> str:
        return self.base_path

    @staticmethod
    def create_if_required(path: str):
        if not os.path.exists(path):
            os.makedirs(path)


class FileCache(object):
    def __init__(self, params: TBeautifulCapiParams):
        self.params = params
        self.base_path = params.output_folder
        self.file2generator = {}

    @staticmethod
    def __get_file_name_base_for_namespace_common(namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        result_folder = join_traits.join_to_base(namespace_path)
        join_traits.create_if_required(result_folder)
        return result_folder

    def __get_file_name_base_for_namespace(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        if self.params.namespace_header_at_parent_folder:
            return FileCache.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits)
        else:
            return FileCache.__get_file_name_base_for_namespace_common(namespace_path, join_traits)

    def __get_file_name_for_namespace(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path, join_traits),
            namespace_path[-1] + '.h'
        )

    def __get_file_name_for_enums(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path, join_traits),
            namespace_path[-1] + self.params.enums_header_suffix + '.h'
        )

    def __get_file_name_for_class_decl(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits),
            replace_template_to_filename(namespace_path[-1]) + self.params.decl_header_suffix + '.h'
        )

    def __get_file_name_for_class(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits),
            replace_template_to_filename(namespace_path[-1]) + '.h'
        )

    def __get_file_name_for_capi(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path[0:1], join_traits),
            namespace_path[0] + self.params.capi_header_suffix + '.h'
        )

    def __get_file_name_for_fwd(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path[0:1], join_traits),
            namespace_path[0] + self.params.fwd_header_suffix + '.h'
        )

    def __get_cached_generator(self, file_name: str) -> FileGenerator:
        if file_name in self.file2generator:
            return self.file2generator[file_name]
        else:
            new_file_generator = FileGenerator(file_name)
            self.file2generator.update({file_name: new_file_generator})
            return new_file_generator

    def get_file_for_root_header(self) -> FileGenerator:
        return self.__get_cached_generator(os.path.join(self.base_path, self.params.root_header))

    def get_file_for_namespace(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_namespace(path_to_namespace, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_enums(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_enums(path_to_namespace, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_class_decl(self, path_to_class: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_class_decl(path_to_class, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_class(self, path_to_class: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_class(path_to_class, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_capi(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_capi(path_to_namespace, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_fwd(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_fwd(path_to_namespace, OsJoin(self.base_path))
        return self.__get_cached_generator(output_file_name)

    def get_file_for_check_and_throw_exception(self) -> FileGenerator:
        return self.__get_cached_generator(os.path.join(self.base_path, self.params.check_and_throw_exception_filename))

    def namespace_header(self, path_to_namespace: [str]) -> str:
        return self.__get_file_name_for_namespace(path_to_namespace, PosixJoin())

    def enums_header(self, path_to_namespace: [str]) -> str:
        return self.__get_file_name_for_enums(path_to_namespace, PosixJoin())

    def class_header_decl(self, path_to_class: [str]) -> str:
        return self.__get_file_name_for_class_decl(path_to_class, PosixJoin())

    def class_header(self, path_to_class: [str]) -> str:
        return self.__get_file_name_for_class(path_to_class, PosixJoin())

    def capi_header(self, path_to_namespace: [str]) -> str:
        return self.__get_file_name_for_capi(path_to_namespace, PosixJoin())

    def fwd_header(self, path_to_namespace: [str]) -> str:
        return self.__get_file_name_for_fwd(path_to_namespace, PosixJoin())

    def check_and_throw_exception_header(self) -> str:
        return self.params.check_and_throw_exception_filename
