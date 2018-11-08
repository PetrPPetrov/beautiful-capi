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
import copy
import random
import uuid
from collections import OrderedDict

from Parser import TBeautifulCapiRoot
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, WatchdogScope, IfDefScope, Indent
from FileGenerator import if_then_else, if_def_then_else, if_not_def_then_else
from DynamicLoaderGenerator import DynamicLoaderGenerator
from StaticLoaderGenerator import StaticLoaderGenerator
from CheckBinaryCompatibilityGenerator import generate_get_version_functions
from FileCache import FileCache
from Helpers import if_required_then_add_empty_line, get_c_name


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
        self.nested_namespaces = []


class CapiGenerator(object):
    def __init__(self, main_exception_traits, no_handling_exception_traits,
                 params: TBeautifulCapiParams, api_root: TBeautifulCapiRoot):
        self.params = params
        self.api_root = api_root
        self.namespace_name_2_info = {}    # type: dict[tuple[str, ...]: NamespaceInfo]
        self.main_exception_traits = main_exception_traits
        self.no_handling_exception_traits = no_handling_exception_traits
        self.additional_defines = FileGenerator(None)
        self.additional_includes = FileGenerator(None)
        self.additional_includes.put_include_files()
        self.additional_includes.include_system_header('stdexcept')
        self.additional_includes.include_system_header('cassert')
        self.main_exception_traits.include_wrap_cpp_headers(self.additional_includes)
        self.callback_implementations = []
        self.cur_api_define = None
        self.cur_api_static = None
        self.cur_capi_prefix = None
        self.cur_api_convention = None
        self.sorted_by_ns = None
        self.cur_namespace_name = None
        self.cur_namespace_info = None
        self.api_keys = {}

    @staticmethod
    def __is_sub_namespace(base_ns_full_name: tuple, ns_full_name: tuple) -> bool:
        if len(base_ns_full_name) != len(ns_full_name) - 1:
            return False
        for i, j in zip(base_ns_full_name, ns_full_name):
            if i != j:
                return False
        return True

    def get_exception_traits(self, no_except: bool):
        if no_except:
            return self.no_handling_exception_traits
        return self.main_exception_traits

    def __generate_posix_i386_attribute(self, out: FileGenerator):
        out.put_line('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))

    def __generate_posix_non_i386_attribute(self, out: FileGenerator):
        out.put_line('#define {0}'.format(self.cur_api_convention))

    def __put_define_apple_or_linux(self, out: FileGenerator):
        out.put_line('#ifdef {0}'.format(self.cur_api_static))
        with Indent(out):
            out.put_line('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
        out.put_line('#else /* normal dynamic mode */')
        with Indent(out):
            out.put_line('#if defined(__GNUC__) && __GNUC__ >= 4')
            with Indent(out):
                out.put_line('#define {0} {1} __attribute__ ((visibility ("default")))'.format(
                    self.cur_api_define, self.cur_capi_prefix))
            out.put_line('#else')
            with Indent(out):
                out.put_line('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
            out.put_line('#endif')
        out.put_line('#endif /* normal dynamic mode */')
        if_def_then_else(out, '__i386__',
                         self.__generate_posix_i386_attribute,
                         self.__generate_posix_non_i386_attribute)

    def __put_api_define(self, out: FileGenerator, dll_import_or_export):
        out.put_line('#ifdef _WIN32')
        with Indent(out):
            out.put_line('#ifdef __GNUC__')
            with Indent(out):
                out.put_line('#ifdef {0}'.format(self.cur_api_static))
                with Indent(out):
                    out.put_line('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
                out.put_line('#else /* normal dynamic mode */')
                with Indent(out):
                    out.put_line('#define {0} {1} __attribute__ (({2}))'.format(
                        self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                out.put_line('#endif /* normal dynamic mode */')
                out.put_line('#define {0} __attribute__ ((cdecl))'.format(self.cur_api_convention))
            out.put_line('#else')
            with Indent(out):
                out.put_line('#ifdef {0}'.format(self.cur_api_static))
                with Indent(out):
                    out.put_line('#define {0} {1}'.format(self.cur_api_define, self.cur_capi_prefix))
                out.put_line('#else /* normal dynamic mode */')
                with Indent(out):
                    out.put_line('#define {0} {1} __declspec({2})'.format(
                        self.cur_api_define, self.cur_capi_prefix, dll_import_or_export))
                out.put_line('#endif /* normal dynamic mode */')
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

    def __generate_callback_typedefs(self, namespace_info: NamespaceInfo, out: FileGenerator):
        for c_pointer in namespace_info.c_pointers:
            out.put_line('typedef {return_type} ({convention} *{name})({arguments});'.format(
                return_type=c_pointer.return_type,
                convention=self.cur_api_convention,
                name=c_pointer.name,
                arguments=c_pointer.arguments))
        if namespace_info.nested_namespaces:
            for nested_ns in namespace_info.nested_namespaces:
                self.__generate_callback_typedefs(nested_ns, out)

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
        self.cur_api_define = '{0}_API'.format(self.cur_namespace_name[0].upper())
        self.cur_api_static = '{0}_STATIC'.format(self.cur_namespace_name[0].upper())
        self.cur_api_convention = '{0}_API_CONVENTION'.format(self.cur_namespace_name[0].upper())
        self.cur_capi_prefix = '{0}_CAPI_PREFIX'.format(self.cur_namespace_name[0].upper())
        if_def_then_else(out, '__cplusplus',
                         self.__generate_capi_c_prefix,
                         self.__generate_capi_prefix)
        out.put_line('')
        self.__put_api_define(out, 'dllimport')

    def __generate_capi_impl_defines(self, out: FileGenerator):
        self.cur_api_define = '{0}_API'.format(self.cur_namespace_name[0].upper())
        self.cur_api_static = '{0}_STATIC'.format(self.cur_namespace_name[0].upper())
        self.cur_api_convention = '{0}_API_CONVENTION'.format(self.cur_namespace_name[0].upper())
        self.cur_capi_prefix = 'extern "C"'
        self.__put_api_define(out, 'dllexport')

    def __generate_function_pointers(self, namespace_info: NamespaceInfo, out: FileGenerator, define: bool):
        for c_function in namespace_info.c_functions:
            if define:
                out.put_line('#ifdef {name}_define_function_pointer_var'.format(name=c_function.name))
                with Indent(out):
                    out.put_line('{name}_define_function_pointer_var'.format(name=c_function.name))
                out.put_line('#else')
                with Indent(out):
                    out.put_line('{name}_function_type {name} = 0;'.format(
                        name=c_function.name, define_to_null_str=' = 0' if define else ''))
                out.put_line('#endif')
            else:
                out.put_line('extern {name}_function_type {name};'.format(name=c_function.name))
        if namespace_info.nested_namespaces:
            for nested_ns in namespace_info.nested_namespaces:
                self.__generate_function_pointers(nested_ns, out, define)

    def __generate_function_pointer_definitions(self, out: FileGenerator):
        out.put_line('')
        self.__generate_function_pointers(self.cur_namespace_info, out, True)
        out.put_line('')

    def __generate_function_pointer_declarations(self, out: FileGenerator):
        out.put_line('')
        self.__generate_function_pointers(self.cur_namespace_info, out, False)
        out.put_line('')

    def __generate_namespace_c_function_pointers(self, namespace_info: NamespaceInfo, out: FileGenerator):
        for c_function in namespace_info.c_functions:
            func_ptr = Pointer2CFunction(
                c_function.path_to_namespace,
                c_function.return_type,
                c_function.name + '_function_type',
                c_function.arguments
            )
            self.cur_namespace_info.c_pointers.append(func_ptr)
            out.put_line('typedef {return_type} ({convention} *{name})({arguments});'.format(
                return_type=func_ptr.return_type,
                convention=self.cur_api_convention,
                name=func_ptr.name,
                arguments=func_ptr.arguments))
        if namespace_info.nested_namespaces:
            for nested_ns in namespace_info.nested_namespaces:
                self.__generate_namespace_c_function_pointers(nested_ns, out)

    def __generate_dynamic_capi(self, out: FileGenerator):
        out.put_line('')
        self.__generate_namespace_c_function_pointers(self.cur_namespace_info, out)
        #self.__generate_callback_typedefs(self.cur_namespace_info, out)
        out.put_line('')
        if_def_then_else(out, self.cur_namespace_name[0].upper() + '_CAPI_DEFINE_FUNCTION_POINTERS',
                         self.__generate_function_pointer_definitions,
                         self.__generate_function_pointer_declarations)
        DynamicLoaderGenerator(self.cur_namespace_name[0], self.cur_namespace_info, self.params).generate(out)

    def __generate_c_functions_for_static_load(self, namespace_info: NamespaceInfo, out: FileGenerator):
        for c_function in namespace_info.c_functions:
            out.put_line('{api} {return_type} {convention} {name}({arguments});'.format(
                api=self.cur_api_define,
                return_type=c_function.return_type,
                convention=self.cur_api_convention,
                name=c_function.name,
                arguments=c_function.arguments))
        if namespace_info.nested_namespaces:
            for nested_ns in namespace_info.nested_namespaces:
                self.__generate_c_functions_for_static_load(nested_ns, out)

    def __generate_static_capi(self, out: FileGenerator):
        self.__generate_c_functions_for_static_load(self.cur_namespace_info, out)
        StaticLoaderGenerator(self.cur_namespace_name[0], self.cur_namespace_info, self.params).generate(out)
        out.put_line('')

    def __generate_msvc1900_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT noexcept'.format(ns=self.cur_namespace_name[0].upper()))

    def __generate_msvc_non1900_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT'.format(ns=self.cur_namespace_name[0].upper()))

    def __generate_msvc1600_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_CPP_COMPILER_HAS_RVALUE_REFERENCES'.format(ns=self.cur_namespace_name[0].upper()))

    def __generate_msvc1800_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE'.format(ns=self.cur_namespace_name[0].upper()))

    def __generate_msvc_traits(self, out: FileGenerator):
        if_then_else(out, '_MSC_VER >= 1900', self.__generate_msvc1900_traits, self.__generate_msvc_non1900_traits)
        if_then_else(out, '_MSC_VER >= 1600', self.__generate_msvc1600_traits, None)
        if_then_else(out, '_MSC_VER >= 1800', self.__generate_msvc1800_traits, None)

    def __generate_cpp11_compiler_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT noexcept'.format(ns=self.cur_namespace_name[0].upper()))
        out.put_line('#define {ns}_CPP_COMPILER_HAS_RVALUE_REFERENCES'.format(ns=self.cur_namespace_name[0].upper()))
        out.put_line('#define {ns}_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE'.format(ns=self.cur_namespace_name[0].upper()))

    def __generate_non_cpp11_compiler_traits(self, out: FileGenerator):
        out.put_line('#define {ns}_NOEXCEPT'.format(ns=self.cur_namespace_name[0].upper()))

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

    def __generate_keys(self):
        if not self.params.open_api:
            namespace_2_keys = {}
            if self.params.root_header:
                root_keys = FileGenerator(os.path.join(
                    self.params.api_keys_folder,
                    os.path.splitext(self.params.root_header)[0] + self.params.key_header_suffix + '.h'))
                root_keys.put_begin_cpp_comments(self.params)
                for namespace_name, namespace_info in self.sorted_by_ns.items():
                    namespace_2_keys.update({namespace_name: root_keys})
            else:
                for namespace_name, namespace_info in self.sorted_by_ns.items():
                    keys = FileGenerator(os.path.join(
                        self.params.api_keys_folder,
                        namespace_info.namespace_name_array[0] + self.params.key_header_suffix + '.h'))
                    keys.put_begin_cpp_comments(self.params)
                    namespace_2_keys.update({namespace_name: keys})
            for namespace_name, namespace_info in self.sorted_by_ns.items():
                self.__generate_keys_for_namespace(namespace_2_keys[namespace_name], namespace_name)

    def __generate_keys_for_namespace(self, out: FileGenerator, namespace_name):
        sorted_by_open_name = OrderedDict(sorted(self.api_keys[namespace_name].items()))
        key_order_list = [
            (opened_name, closed_name) for opened_name, closed_name in sorted_by_open_name.items()]
        random.shuffle(key_order_list)
        define_order_list = [opened_name for opened_name, closed_name in key_order_list]
        random.shuffle(define_order_list)
        define_order_list_to_substitute = copy.deepcopy(define_order_list)
        random.shuffle(define_order_list_to_substitute)
        load_order_list = copy.deepcopy(define_order_list_to_substitute)
        random.shuffle(load_order_list)
        load_order_list_to_substitute = copy.deepcopy(load_order_list)
        random.shuffle(load_order_list_to_substitute)
        zero_order_list = copy.deepcopy(load_order_list_to_substitute)
        random.shuffle(zero_order_list)
        zero_order_list_to_substitute = copy.deepcopy(zero_order_list)
        random.shuffle(zero_order_list_to_substitute)
        for opened_name, closed_name in key_order_list:
            out.put_line('#define {opened_name} {closed_name}'.format(
                opened_name=opened_name, closed_name=closed_name
            ))
            out.put_line('#define {opened_name}_closed_name "{closed_name}"'.format(
                opened_name=opened_name, closed_name=closed_name
            ))
        define_order = zip(define_order_list, define_order_list_to_substitute)
        for opened_name, opened_name_to_substitute in define_order:
            out.put_line('#define {0}_define_function_pointer_var {1}_function_type {1} = 0;'.format(
                opened_name, opened_name_to_substitute
            ))
        load_order = zip(load_order_list, load_order_list_to_substitute)
        for opened_name, opened_name_to_substitute in load_order:
            out.put_line(
                '#define {0}_load_function_call load_function<{1}_function_type>({1}, {1}_closed_name);'.format(
                    opened_name, opened_name_to_substitute))
        zero_order = zip(zero_order_list, zero_order_list_to_substitute)
        for opened_name, opened_name_to_substitute in zero_order:
            out.put_line('#define {0}_zero_function_pointer {1} = 0;'.format(opened_name, opened_name_to_substitute))

    def __generate_capi(self, file_cache):
        sorted_by_ns = OrderedDict(sorted(self.namespace_name_2_info.items()))
        for namespace_name, namespace_info in sorted_by_ns.items():
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            if len(namespace_name) == 1:
                output_capi = file_cache.get_file_for_capi(namespace_name)
                output_capi.put_begin_cpp_comments(self.params)
                with WatchdogScope(output_capi, '_'.join(namespace_name).upper() + '_CAPI_INCLUDED'):
                    output_capi.put_include_files()
                    output_capi.include_system_header('stddef.h')
                    self.main_exception_traits.generate_exception_info(output_capi)
                    self.__generate_capi_defines(output_capi)
                    self.__generate_version_defines(output_capi, '_'.join(namespace_name).upper())
                    self.__generate_compiler_traits(output_capi)

                    output_capi.put_line('')
                    self.__generate_callback_typedefs(self.cur_namespace_info, output_capi)
                    output_capi.put_line('')

                    if_not_def_then_else(output_capi, '_'.join(namespace_name).upper() + '_CAPI_USE_DYNAMIC_LOADER',
                                         self.__generate_static_capi,
                                         self.__generate_dynamic_capi)
        self.__generate_keys()

    def __generate_capi_impl_functions(self, functions_list, namespace_name, namespace_info, out: FileGenerator):
        file_count = 0
        dot_index = out.filename.rfind('.')
        filename_format_str = '{0}{{count}}{1}'.format(out.filename[:dot_index], out.filename[dot_index:])
        cur_size = out.line_count()
        for c_function in functions_list:
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            generated_name = c_function.name
            if not self.params.open_api:
                generated_name = get_c_name('fx' + str(uuid.uuid4()))
                if namespace_name not in self.api_keys:
                    self.api_keys.update({namespace_name: {}})
                self.api_keys[namespace_name][c_function.name] = generated_name
            c_function_size = c_function.body.line_count() + 1
            if cur_size + c_function_size > self.params.wrap_file_line_limit:
                file_count += 1
                filename = filename_format_str.format(count=file_count)
                out.put_line('#include "{}"'.format(os.path.split(filename)[1]))
                out = FileGenerator(filename)
                cur_size = 0
            out.put_line('{api} {return_type} {convention} {name}({arguments})'.format(
                api=self.cur_api_define,
                return_type=c_function.return_type,
                convention=self.cur_api_convention,
                name=generated_name,
                arguments=c_function.arguments))
            out.put_file(c_function.body)
            cur_size += c_function_size
        for nested_ns in self.namespace_name_2_info.keys():
            if self.__is_sub_namespace(namespace_name, nested_ns):
                out.put_line('#include "{}"'.format('/'.join([namespace_name[-1], nested_ns[-1] + 'Wrap.h'])))

    def __generate_capi_with_file_separation(self, main_out: FileGenerator, file_cache: FileCache):
        for namespace_name, namespace_info in self.namespace_name_2_info.items():
            namespace_path = ['AutoGenWrap'] + list(namespace_name[:-1]) + [namespace_name[-1] + 'Wrap.h']
            filename = file_cache.get_file_for_capi_namespace(namespace_path)
            out = FileGenerator(filename)
            plain_functions_list = copy.copy(namespace_info.c_functions)
            if not self.params.open_api:
                random.shuffle(plain_functions_list)
            self.__generate_capi_impl_functions(plain_functions_list, namespace_name, namespace_info, out)
            if len(namespace_name) == 1:
                main_out.put_line('#include "{}"'.format('/'.join(namespace_path)))

    def __generate_capi_impl(self, out: FileGenerator):
        plain_functions_list = []
        sorted_by_ns = OrderedDict(sorted(self.namespace_name_2_info.items()))
        for namespace_name, namespace_info in sorted_by_ns.items():
            for c_function in namespace_info.c_functions:
                plain_functions_list.append(c_function)
        if not self.params.open_api:
            random.shuffle(plain_functions_list)
        self.__generate_capi_impl_functions(plain_functions_list, self.cur_namespace_name, self.cur_namespace_info, out)

    def __create_parent_ns_info_if_not_exist(self, path_to_namespace: [str]):
        parent = tuple(path_to_namespace[:-1])
        if len(parent) > 0:
            if not self.namespace_name_2_info.get(parent, None):
                self.namespace_name_2_info[parent] = NamespaceInfo()
            self.__create_parent_ns_info_if_not_exist(parent)

    def add_c_function(self, path_to_namespace: [str], return_type: str,
                       name: str, arguments: str, body: FileGenerator):
        new_c_function = CFunction(path_to_namespace, return_type, name, arguments, body)
        namespace_name = tuple(path_to_namespace)  # We always have at least one element
        if namespace_name not in self.namespace_name_2_info:
            new_namespace_info = NamespaceInfo()
            new_namespace_info.namespace_name_array = copy.deepcopy(path_to_namespace)
            new_namespace_info.c_functions.append(new_c_function)
            self.namespace_name_2_info.update({namespace_name: new_namespace_info})
        else:
            self.namespace_name_2_info[namespace_name].c_functions.append(new_c_function)
        self.__create_parent_ns_info_if_not_exist(path_to_namespace)

    def add_c_function_pointer(self, path_to_namespace: [str], return_type: str, name: str, arguments: str):
        new_c_pointer = Pointer2CFunction(path_to_namespace, return_type, name, arguments)
        namespace_name = tuple(path_to_namespace)  # We always have at least one element
        if namespace_name not in self.namespace_name_2_info:
            new_namespace_info = NamespaceInfo()
            new_namespace_info.namespace_name_array = copy.deepcopy(path_to_namespace)
            new_namespace_info.c_pointers.append(new_c_pointer)
            self.namespace_name_2_info.update({namespace_name: new_namespace_info})
        else:
            self.namespace_name_2_info[namespace_name].c_pointers.append(new_c_pointer)
        self.__create_parent_ns_info_if_not_exist(path_to_namespace)

    def generate(self, file_cache: FileCache):
        self.main_exception_traits.generate_check_and_throw_exception(file_cache)

        output_capi_impl = FileGenerator(self.params.output_wrap_file_name)
        output_capi_impl.put_begin_cpp_comments(self.params)
        output_capi_impl.put_file(self.additional_defines)
        output_capi_impl.put_file(self.additional_includes)
        self.main_exception_traits.generate_exception_info(output_capi_impl)

        for namespace_name, namespace_info in self.namespace_name_2_info.items():
            parent_name = namespace_name[0:-1]
            if len(parent_name) > 0:
                if not self.namespace_name_2_info.get(parent_name, None):
                    new_namespace_info = NamespaceInfo()
                    new_namespace_info.namespace_name_array = parent_name
                    self.namespace_name_2_info[parent_name] = new_namespace_info
                self.namespace_name_2_info[parent_name].nested_namespaces.append(namespace_info)
        sorted_by_ns = OrderedDict(sorted(self.namespace_name_2_info.items()))
        for namespace_name, namespace_info in sorted_by_ns.items():
            self.cur_namespace_name = namespace_name
            self.cur_namespace_info = namespace_info
            if len(namespace_name) == 1:
                self.__generate_capi_impl_defines(output_capi_impl)
                generate_get_version_functions(
                    output_capi_impl, namespace_name[0], self.params, self.api_root)
            self.__generate_callback_typedefs(namespace_info, output_capi_impl)

        self.__generate_callback_implementations(output_capi_impl)
        if self.params.split_wrap_by_namespaces:
            self.__generate_capi_with_file_separation(output_capi_impl, file_cache)
        else:
            self.__generate_capi_impl(output_capi_impl)
        self.__generate_capi(file_cache)
