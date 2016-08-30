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

from TraitsBase import TraitsBase
import FileGenerator


class CfunctionTraitsBase(TraitsBase):
    def __init__(self, capi_generator):
        super().__init__(None, capi_generator)


class ImplLib(CfunctionTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)
        self.cur_api_define = None
        self.cur_api_convention = None
        self.cur_api_declarations = None
        self.cur_capi_prefix = None
        self.impl_headers = None

    def __put_define_apple_or_linux(self, indent_function, put_function):
        put_function('#if defined(__GNUC__) && __GNUC__ >= 4')
        with indent_function():
            put_function('#define {0} {1} __attribute__ ((visibility ("default")))'.format(
                self.cur_api_define, self.cur_capi_prefix))
        put_function('#else')
        with indent_function():
            put_function('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
        put_function('#endif')
        put_function('#if defined __i386__')
        with indent_function():
            put_function('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))
        put_function('#else')
        with indent_function():
            put_function('#define {0}'.format(self.cur_api_convention))
        put_function('#endif')

    def __put_api_define(self, put_function, indent_function, dll_import_or_export):
        put_function('#ifdef _WIN32')
        with indent_function():
            put_function('#ifdef __GNUC__')
            with indent_function():
                put_function('#define {0} {1} __attribute__ (({2}))'.format(
                    self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                put_function('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))
            put_function('#else')
            with indent_function():
                put_function('#define {0} {1} __declspec({2})'.format(
                    self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                put_function('#define {0} __cdecl'.format(self.cur_api_convention))
            put_function('#endif')
        put_function('#elif __APPLE__')
        with indent_function():
            self.__put_define_apple_or_linux(indent_function, put_function)
        put_function('#elif __unix__ || __linux__')
        with indent_function():
            self.__put_define_apple_or_linux(indent_function, put_function)
        put_function('#else')
        with indent_function():
            put_function('#error "Unknown platform"')
        put_function('#endif')
        put_function('')

    def generate_c_functions_declarations(self):
        self.capi_generator.output_source.include_system_header('stdexcept')
        self.capi_generator.output_source.include_system_header('cassert')
        self.capi_generator.output_source.put_include_files()
        self.impl_headers = self.capi_generator.output_source
        self.put_source_line('')

        if not self.capi_generator.c_enums.empty():
            self.put_file(self.capi_generator.c_enums)

        if not self.capi_generator.callback_typedefs.empty():
            self.capi_generator.callback_typedefs.put_line('')
            self.put_file(self.capi_generator.callback_typedefs)

        self.cur_api_define = '{0}_API'.format(self.capi_generator.get_namespace_id().upper())
        self.cur_api_convention = '{0}_API_CONVENTION'.format(self.capi_generator.get_namespace_id().upper())
        self.cur_capi_prefix = 'extern "C"'
        self.__put_api_define(self.put_source_line, self.indent_source, 'dllexport')

        self.cur_capi_prefix = '{0}_CAPI_PREFIX'.format(self.capi_generator.get_namespace_id().upper())
        self.put_line('#ifdef __cplusplus')
        with self.indent():
            self.put_line('#define {0} extern "C"'.format(self.cur_capi_prefix))
        self.put_line('#else')
        with self.indent():
            self.put_line('#define {0}'.format(self.cur_capi_prefix))
        self.put_line('#endif')
        self.put_line('')
        self.__put_api_define(self.put_line, self.indent, 'dllimport')

        self.cur_api_declarations = FileGenerator.FileGenerator(None)
        self.put_file(self.cur_api_declarations)
        if not self.capi_generator.api_defines_generated:
            self.put_source_file(self.capi_generator.callback_typedefs)
            self.put_source_file(self.capi_generator.callbacks_implementations)
        self.capi_generator.api_defines_generated = True

    def add_c_function_declaration(self, declaration):
        declaration_with_convention = declaration.format(convention=self.cur_api_convention)
        self.cur_api_declarations.put_line('{0} {1};'.format(self.cur_api_define, declaration_with_convention))
        self.put_source_line('{0} {1}'.format(self.cur_api_define, declaration_with_convention))

    def add_impl_header(self, implementation_header):
        if implementation_header:
            self.impl_headers.include_user_header(implementation_header)


class DynamicLoad(CfunctionTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)

    def generate_c_functions_declarations(self):
        pass


def create_loader_traits(capi_generator):
    if capi_generator.params_description.dynamically_load_functions:
        return DynamicLoad(capi_generator)
    else:
        return ImplLib(capi_generator)


class CreateLoaderTraits(object):
    def __init__(self, capi_generator):
        self.capi_generator = capi_generator
        self.previous_loader_traits = capi_generator.loader_traits

    def __enter__(self):
        self.capi_generator.loader_traits = create_loader_traits(self.capi_generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capi_generator.loader_traits = self.previous_loader_traits
