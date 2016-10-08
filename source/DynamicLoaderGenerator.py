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


from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IfDefScope, IndentScope, Indent, Unindent
from FileGenerator import if_def_then_else
from CheckBinaryCompatibilityGenerator import generate_check_version


class DynamicLoaderGenerator(object):
    def __init__(self, namespace_name, namespace_info, params: TBeautifulCapiParams):
        self.namespace_name = namespace_name
        self.namespace_info = namespace_info
        self.params = params
        self.cur_c_function_name = None

    @staticmethod
    def __generate_windows_members(out: FileGenerator):
        out.put_line('HINSTANCE handle;')

    @staticmethod
    def __generate_posix_members(out: FileGenerator):
        out.put_line('void* handle;')

    @staticmethod
    def __generate_members(out: FileGenerator):
        if_def_then_else(out, '_WIN32',
                         DynamicLoaderGenerator.__generate_windows_members,
                         DynamicLoaderGenerator.__generate_posix_members)
        out.put_line('')

    @staticmethod
    def __generate_load_function_windows(out: FileGenerator):
        out.put_line('to_init = reinterpret_cast<FunctionPointerType>(GetProcAddress(handle, name));')

    @staticmethod
    def __generate_load_function_posix(out: FileGenerator):
        out.put_line('to_init = reinterpret_cast<FunctionPointerType>(dlsym(handle, name));')

    @staticmethod
    def __generate_load_function(out: FileGenerator):
        out.put_line('template<class FunctionPointerType>')
        out.put_line('void load_function(FunctionPointerType& to_init, const char* name)')
        with IndentScope(out):
            if_def_then_else(out, '_WIN32',
                             DynamicLoaderGenerator.__generate_load_function_windows,
                             DynamicLoaderGenerator.__generate_load_function_posix)
            out.put_line('if (!to_init)')
            with IndentScope(out):
                out.put_line('std::stringstream error_message;')
                out.put_line('error_message << "Can\'t obtain function " << name;')
                out.put_line('throw std::runtime_error(error_message.str());')
        out.put_line('')

    @staticmethod
    def __generate_load_module_windows(out: FileGenerator):
        out.put_line('handle = LoadLibraryA(shared_library_name);')

    @staticmethod
    def __generate_load_module_posix(out: FileGenerator):
        out.put_line('handle = dlopen(shared_library_name, RTLD_NOW);')

    def __generate_secure_load(self, out: FileGenerator):
        out.put_line('load_function<{0}_function_type>({0}, {0}_str);'.format(self.cur_c_function_name))

    def __generate_open_load(self, out: FileGenerator):
        out.put_line('load_function<{0}_function_type>({0}, "{0}");'.format(self.cur_c_function_name))

    def __generate_load_module(self, out: FileGenerator):
        out.put_line('void load_module(const char* shared_library_name)')
        with IndentScope(out):
            out.put_line('if (!shared_library_name) throw std::runtime_error("Null library name was passed");')
            if_def_then_else(out, '_WIN32',
                             DynamicLoaderGenerator.__generate_load_module_windows,
                             DynamicLoaderGenerator.__generate_load_module_posix)
            out.put_line('if (!handle)')
            with IndentScope(out):
                out.put_line('std::stringstream error_message;')
                out.put_line('error_message << "Can\'t load shared library " << shared_library_name;')
                out.put_line('throw std::runtime_error(error_message.str());')
            for c_function in self.namespace_info.c_functions:
                self.cur_c_function_name = c_function.name
                if_def_then_else(out, "{0}_str".format(c_function.name),
                                 self.__generate_secure_load,
                                 self.__generate_open_load)
            generate_check_version(out, self.namespace_info.namespace_name_array[0], 'shared_library_name')
        out.put_line('')

    def __generate_constructor(self, out: FileGenerator):
        out.put_line('Initialization(const char* shared_library_name)')
        with IndentScope(out):
            out.put_line('load_module(shared_library_name);')
        if self.params.shared_library_name:
            out.put_line('Initialization()')
            with IndentScope(out):
                out.put_line('#ifdef _WIN32')
                with Indent(out):
                    out.put_line('load_module("{shared_library_name}.dll");'.format(
                        shared_library_name=self.params.shared_library_name))
                out.put_line('#elif __APPLE__')
                with Indent(out):
                    out.put_line('load_module("lib{shared_library_name}.dylib");'.format(
                        shared_library_name=self.params.shared_library_name))
                out.put_line('#else')
                with Indent(out):
                    out.put_line('load_module("lib{shared_library_name}.so");'.format(
                        shared_library_name=self.params.shared_library_name))
                out.put_line('#endif')

    @staticmethod
    def __generate_destructor_windows(out: FileGenerator):
        out.put_line('FreeLibrary(handle);')

    @staticmethod
    def __generate_destructor_posix(out: FileGenerator):
        out.put_line('dlclose(handle);')

    def __generate_destructor(self, out: FileGenerator):
        out.put_line('~Initialization()')
        with IndentScope(out):
            if_def_then_else(out, '_WIN32',
                             DynamicLoaderGenerator.__generate_destructor_windows,
                             DynamicLoaderGenerator.__generate_destructor_posix)
            for c_function in self.namespace_info.c_functions:
                out.put_line('{0} = 0;'.format(c_function.name))

    def __generate_body(self, out: FileGenerator):
        out.put_line('class Initialization')
        with IndentScope(out, '};'):
            self.__generate_members(out)
            self.__generate_load_function(out)
            self.__generate_load_module(out)
            if not self.params.shared_library_name:
                out.put_line('Initialization();')
            out.put_line('Initialization(const Initialization&);')
            if self.params.enable_cpp11_features_in_wrap_code:
                move_constructors_delete_condition = '{ns}_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE'.format(
                    ns=self.namespace_name)
                with IfDefScope(out, move_constructors_delete_condition, False):
                    with Indent(out):
                        out.put_line('Initialization(Initialization &&) = delete;')
            with Unindent(out):
                out.put_line('public:')
            self.__generate_constructor(out)
            self.__generate_destructor(out)

    @staticmethod
    def __generate_windows_includes(out: FileGenerator):
        out.put_line('#include <Windows.h>')

    @staticmethod
    def __generate_posix_includes(out: FileGenerator):
        out.put_line('#include <dlfcn.h>')

    def generate(self, out: FileGenerator):
        out.put_line('')
        with IfDefScope(out, '__cplusplus'):
            out.put_line('#include <stdexcept>')
            out.put_line('#include <sstream>')
            out.put_line('')
            if_def_then_else(out, '_WIN32', self.__generate_windows_includes, self.__generate_posix_includes)
            out.put_line('')
            # We always have at least one element
            out.put_line('namespace {0}'.format(self.namespace_info.namespace_name_array[0]))
            with IndentScope(out):
                self.__generate_body(out)
