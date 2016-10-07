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


import copy
from collections import OrderedDict
from Parser import TBeautifulCapiRoot
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, WatchdogScope, IfDefScope, Indent
from FileGenerator import if_then_else, if_def_then_else, if_not_def_then_else
from DynamicLoaderGenerator import DynamicLoaderGenerator
from StaticLoaderGenerator import StaticLoaderGenerator
from CheckBinaryCompatibilityGenerator import generate_get_version_functions
from FileCache import FileCache
from Helpers import if_required_then_add_empty_line


class CFunction(object):
    def __init__(self, path_to_namespace: [str], return_type: str, name: str, arguments: str, body: FileGenerator):
        self.path_to_namespace = path_to_namespace
        self.return_type = return_type
        self.name = name
        self.arguments = arguments
        self.body = body


class Pointer2CFunction(object):
    def __init__(self, path_to_namespace: [str], return_type: str, name: str, arguments: str):
        self.path_to_namespace = path_to_namespace
        self.return_type = return_type
        self.name = name
        self.arguments = arguments


class NamespaceInfo(object):
    def __init__(self):
        self.namespace_name_array = []
        self.c_functions = []
        self.c_pointers = []


class CapiGenerator(object):
    def __init__(self, main_exception_traits, no_handling_exception_traits,
                 params: TBeautifulCapiParams, api_root: TBeautifulCapiRoot):
        self.params = params
        self.api_root = api_root
        self.namespace_name_2_info = {}
        self.main_exception_traits = main_exception_traits
        self.no_handling_exception_traits = no_handling_exception_traits
        self.additional_includes = FileGenerator(None)
        self.additional_includes.put_include_files()
        self.additional_includes.include_system_header('stdexcept')
        self.additional_includes.include_system_header('cassert')
        self.callback_implementations = []
        self.cur_api_define = None
        self.cur_capi_prefix = None
        self.cur_api_convention = None
        self.sorted_by_ns = None
        self.cur_namespace_name = None
        self.cur_namespace_info = None

    def get_exception_traits(self, no_except: bool):
        if no_except:
            return self.no_handling_exception_traits
        return self.main_exception_traits

    def __generate_posix_i386_attribute(self, out: FileGenerator):
        out.put_line('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))

    def __generate_posix_non_i386_attribute(self, out: FileGenerator):
        out.put_line('#define {0}'.format(self.cur_api_convention))

    def __put_define_apple_or_linux(self, out: FileGenerator):
        out.put_line('#if defined(__GNUC__) && __GNUC__ >= 4')
        with Indent(out):
            out.put_line('#define {0} {1} __attribute__ ((visibility ("default")))'.format(
                self.cur_api_define, self.cur_capi_prefix))
        out.put_line('#else')
        with Indent(out):
            out.put_line('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
        out.put_line('#endif')
        if_def_then_else(out, '__i386__',
                         self.__generate_posix_i386_attribute,
                         self.__generate_posix_non_i386_attribute)

    def __put_api_define(self, out: FileGenerator, dll_import_or_export):
        out.put_line('#ifdef _WIN32')
        with Indent(out):
            out.put_line('#ifdef __GNUC__')
            with Indent(out):
                out.put_line('#define {0} {1} __attribute__ (({2}))'.format(
                    self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                out.put_line('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))
            out.put_line('#else')
            with Indent(out):
                out.put_line('#define {0} {1} __declspec({2})'.format(
                    self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                out.put_line('#define {0} __cdecl'.format(self.cur_api_convention))
            out.put_line('#endif')
        out.put_line('#elif __APPLE__')
        with Indent(out):
            self.__put_define_apple_or_linux(out)
        out.put_line('#elif __unix__ || __linux__')
        with Indent(out):
            self.__put_define_apple_or_linux(out)
        out.put_line('#else')
        with Indent(out):
            out.put_line('#error "Unknown platform"')
        out.put_line('#endif')
        out.put_line('')

    def __generate_callback_typedefs(self, out: FileGenerator):
        for c_pointer in self.cur_namespace_info.c_pointers:
            out.put_line('typedef {return_type} ({convention} *{name})({arguments});'.format(
                return_type=c_pointer.return_type,
                convention=self.cur_api_convention,
                name=c_pointer.name,
                arguments=c_pointer.arguments))
        if self.cur_namespace_info.c_pointers:
            out.put_line('')

    def __generate_callback_implementations(self, out: FileGenerator):
        if self.callback_implementations:
            self.main_exception_traits.generate_check_and_throw_exception_for_impl(out)
            out.put_line('')
        for callback_implementation in self.callback_implementations:
            out.put_file(callback_implementation)
            out.put_line('')

    def __generate_capi_c_prefix(self, out: FileGenerator):
        out.put_line('#define {0} extern "C"'.format(self.cur_capi_prefix))

    def __generate_capi_prefix(self, out: FileGenerator):
        out.put_line('#define {0}'.format(self.cur_capi_prefix))

    def __generate_capi_defines(self, out: FileGenerator):
        self.cur_api_define = '{0}_API'.format(self.cur_namespace_name)
        self.cur_api_convention = '{0}_API_CONVENTION'.format(self.cur_namespace_name)
        self.cur_capi_prefix = '{0}_CAPI_PREFIX'.format(self.cur_namespace_name)
        if_def_then_else(out, '__cplusplus',
                         self.__generate_capi_c_prefix,
                         self.__generate_capi_prefix)
        out.put_line('')
        self.__put_api_define(out, 'dllimport')

    def __generate_capi_impl_defines(self, out: FileGenerator):
        self.cur_api_define = '{0}_API'.format(self.cur_namespace_name)
        self.cur_api_convention = '{0}_API_CONVENTION'.format(self.cur_namespace_name)
        self.cur_capi_prefix = 'extern "C"'
        self.__put_api_define(out, 'dllexport')

    def __generate_function_pointers(self, out: FileGenerator, define: bool):
        out.put_line('')
        for c_function in self.cur_namespace_info.c_functions:
            out.put_line('extern {name}_function_type {name}{define_to_null_str};'.format(
                name=c_function.name, define_to_null_str=' = 0' if define else ''))
        out.put_line('')

    def __generate_function_pointer_definitions(self, out: FileGenerator):
        self.__generate_function_pointers(out, True)

    def __generate_function_pointer_declarations(self, out: FileGenerator):
        self.__generate_function_pointers(out, False)

    def __generate_dynamic_capi(self, out: FileGenerator):
        out.put_line('')
        for c_function in self.cur_namespace_info.c_functions:
            self.cur_namespace_info.c_pointers.append(
                Pointer2CFunction(
                    c_function.path_to_namespace,
                    c_function.return_type,
                    c_function.name + '_function_type',
                    c_function.arguments
                )
            )
        self.__generate_callback_typedefs(out)
        if_def_then_else(out, self.cur_namespace_name + '_CAPI_DEFINE_FUNCTION_POINTERS',
                         self.__generate_function_pointer_definitions,
                         self.__generate_function_pointer_declarations)

        DynamicLoaderGenerator(self.cur_namespace_name, self.cur_namespace_info, self.params).generate(out)
        out.put_line('')

    def __generate_static_capi(self, out: FileGenerator):
        out.put_line('')
        self.__generate_callback_typedefs(out)
        for c_function in self.cur_namespace_info.c_functions:
            out.put_line('{api} {return_type} {convention} {name}({arguments});'.format(
                api=self.cur_api_define,
                return_type=c_function.return_type,
                convention=self.cur_api_convention,
                name=c_function.name,
                arguments=c_function.arguments))
        StaticLoaderGenerator(self.cur_namespace_name, self.cur_namespace_info, self.params).generate(out)
        out.put_line('')

    def __generate_msvc1900_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT noexcept'.format(ns=self.cur_namespace_name))

    def __generate_msvc_non1900_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT'.format(ns=self.cur_namespace_name))

    def __generate_msvc1600_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_CPP_COMPILER_HAS_RVALUE_REFERENCES'.format(ns=self.cur_namespace_name))

    def __generate_msvc1800_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE'.format(ns=self.cur_namespace_name))

    def __generate_msvc_traits(self, out: FileGenerator):
        if_then_else(out, '_MSC_VER >= 1900', self.__generate_msvc1900_traits, self.__generate_msvc_non1900_traits)
        if_then_else(out, '_MSC_VER >= 1600', self.__generate_msvc1600_traits, None)
        if_then_else(out, '_MSC_VER >= 1800', self.__generate_msvc1800_traits, None)

    def __generate_cpp11_compiler_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT noexcept'.format(ns=self.cur_namespace_name))
        out.put_line('#define {ns}_CPP_COMPILER_HAS_RVALUE_REFERENCES'.format(ns=self.cur_namespace_name))
        out.put_line('#define {ns}_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE'.format(ns=self.cur_namespace_name))

    def __generate_non_cpp11_compiler_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT'.format(ns=self.cur_namespace_name))

    def __generate_non_msvc_traits(self, out: FileGenerator):
        if_then_else(out, '__cplusplus >= 201103L',
                     self.__generate_cpp11_compiler_traits, self.__generate_non_cpp11_compiler_traits)

    def __generate_compiler_traits(self, out: FileGenerator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, '__cplusplus', False):
                with Indent(out):
                    if_def_then_else(out, '_MSC_VER', self.__generate_msvc_traits, self.__generate_non_msvc_traits)
            out.put_line('')

    @staticmethod
    def __generate_version_define(out: FileGenerator, namespace_name: str, name: str, value):
        out.put_line('#define {ns}_{name}_VERSION {value}'.format(
            ns=namespace_name, name=name.upper(), value=value))

    def __generate_version_defines(self, out: FileGenerator, namespace_name: str):
        self.__generate_version_define(out, namespace_name, 'Major', self.api_root.major_version)
        self.__generate_version_define(out, namespace_name, 'Minor', self.api_root.minor_version)
        self.__generate_version_define(out, namespace_name, 'Patch', self.api_root.patch_version)
        out.put_line('')

    def __generate_capi(self, file_cache):
        for namespace_name, namespace_info in self.sorted_by_ns.items():
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            # We always have at least one element
            output_capi = file_cache.get_file_for_capi(namespace_info.c_functions[0].path_to_namespace)
            output_capi.put_begin_cpp_comments(self.params)
            with WatchdogScope(output_capi, namespace_name + '_CAPI_INCLUDED'):
                self.main_exception_traits.generate_exception_info(output_capi)
                self.__generate_capi_defines(output_capi)
                self.__generate_version_defines(output_capi, namespace_name)
                self.__generate_compiler_traits(output_capi)

                if_not_def_then_else(output_capi, namespace_name + '_CAPI_USE_DYNAMIC_LOADER',
                                     self.__generate_static_capi,
                                     self.__generate_dynamic_capi)

    def __generate_capi_impl(self, out: FileGenerator):
        first_namespace = True
        for namespace_name, namespace_info in self.sorted_by_ns.items():
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            first_namespace = if_required_then_add_empty_line(first_namespace, out)
            first_function = True
            for c_function in namespace_info.c_functions:
                first_function = if_required_then_add_empty_line(first_function, out)

                out.put_line('{api} {return_type} {convention} {name}({arguments})'.format(
                    api=self.cur_api_define,
                    return_type=c_function.return_type,
                    convention=self.cur_api_convention,
                    name=c_function.name,
                    arguments=c_function.arguments))
                out.put_file(c_function.body)

    def add_c_function(self, path_to_namespace: [str], return_type: str,
                       name: str, arguments: str, body: FileGenerator):
        new_c_function = CFunction(path_to_namespace, return_type, name, arguments, body)
        namespace_name = path_to_namespace[0].upper()  # We always have at least one element
        if namespace_name not in self.namespace_name_2_info:
            new_namespace_info = NamespaceInfo()
            new_namespace_info.namespace_name_array = copy.deepcopy(path_to_namespace)
            new_namespace_info.c_functions.append(new_c_function)
            self.namespace_name_2_info.update({namespace_name: new_namespace_info})
        else:
            self.namespace_name_2_info[namespace_name].c_functions.append(new_c_function)

    def add_c_function_pointer(self, path_to_namespace: [str], return_type: str, name: str, arguments: str):
        new_c_pointer = Pointer2CFunction(path_to_namespace, return_type, name, arguments)
        namespace_name = path_to_namespace[0].upper()  # We always have at least one element
        if namespace_name not in self.namespace_name_2_info:
            new_namespace_info = NamespaceInfo()
            new_namespace_info.namespace_name_array = copy.deepcopy(path_to_namespace)
            new_namespace_info.c_pointers.append(new_c_pointer)
            self.namespace_name_2_info.update({namespace_name: new_namespace_info})
        else:
            self.namespace_name_2_info[namespace_name].c_pointers.append(new_c_pointer)

    def generate(self, file_cache: FileCache):
        self.main_exception_traits.generate_check_and_throw_exception(file_cache)

        output_capi_impl = FileGenerator(self.params.output_wrap_file_name)
        output_capi_impl.put_begin_cpp_comments(self.params)
        output_capi_impl.put_file(self.additional_includes)
        self.main_exception_traits.generate_exception_info(output_capi_impl)

        self.sorted_by_ns = OrderedDict(sorted(self.namespace_name_2_info.items()))
        for namespace_name, namespace_info in self.sorted_by_ns.items():
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            self.__generate_capi_impl_defines(output_capi_impl)
            self.__generate_callback_typedefs(output_capi_impl)
            generate_get_version_functions(
                output_capi_impl, namespace_info.namespace_name_array[0], self.params, self.api_root)

        self.__generate_callback_implementations(output_capi_impl)
        self.__generate_capi_impl(output_capi_impl)
        self.__generate_capi(file_cache)
