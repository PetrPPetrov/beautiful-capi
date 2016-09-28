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
from FileCache import FileCache
from FileGenerator import FileGenerator, IndentScope, WatchdogScope, IfDefScope, Indent
from ArgumentGenerator import ClassTypeGenerator, BuiltinTypeGenerator
from NamespaceGenerator import NamespaceGenerator
from ClassGenerator import ClassGenerator


class NoHandling(object):
    def __init__(self):
        pass

    def generate_exception_info(self, out: FileGenerator):
        pass

    def generate_check_and_throw_exception_forward_declaration(self, out: FileGenerator):
        pass

    def generate_check_and_throw_exception(self, file_cache: FileCache):
        pass

    @staticmethod
    def generate_c_call(out: FileGenerator, return_type: ClassTypeGenerator or BuiltinTypeGenerator,
                        c_function_name: str, arguments: [str]) -> str:
        c_function_call = '{function_name}({arguments})'.format(
            function_name=c_function_name,
            arguments=', '.join(arguments)
        )
        casting_instructions, return_expression = return_type.c_2_wrap_var('', c_function_call)
        out.put_lines(casting_instructions)
        return return_expression

    @staticmethod
    def modify_c_arguments(arguments: [str]):
        pass

    @staticmethod
    def generate_implementation_call(out: FileGenerator,
                                     return_type: ClassTypeGenerator or BuiltinTypeGenerator, methods_calls: str):
        for method_call in methods_calls:
            out.put_line(method_call)

    def include_dependent_implementation_headers(self, file_generator: FileGenerator):
        pass


class ByFirstArgument(object):
    def __init__(self, params: TBeautifulCapiParams, root_namespace_generators: [NamespaceGenerator]):
        self.params = params
        self.root_namespace_generators = root_namespace_generators
        self.exception_classes = []
        self.exception_classes_generated = False

    def __exception_info_t(self):
        return self.params.beautiful_capi_namespace.lower() + '_exception_info_t'

    def __exception_code_t(self):
        return self.params.beautiful_capi_namespace.lower() + '_exception_code_t'

    def generate_exception_info(self, out: FileGenerator):
        with WatchdogScope(out, '{0}_EXCEPTION_INFO_DEFINED'.format(
                self.params.beautiful_capi_namespace.upper())):
            out.put_line('struct {0}'.format(self.__exception_info_t()))
            with IndentScope(out, '};'):
                out.put_line('int code; /* value from {0} enumeration */'.format(self.__exception_code_t()))
                out.put_line('void* object_pointer;')
            out.put_line('')
            out.put_line('enum {0}'.format(self.__exception_code_t()))
            with IndentScope(out, '};'):
                out.put_line('no_exception = 0,')
                code_to_exception = {exception_class.exception_code: exception_class for exception_class
                                     in self.exception_classes}
                for code, exception_class in code_to_exception.items():
                    out.put_line('{0} = {1},'.format(exception_class.full_c_name, code))
                out.put_line('unknown_exception = -1')

    def generate_check_and_throw_exception_forward_declaration(self, out: FileGenerator):
        watchdog_string = '{0}_CHECK_AND_THROW_EXCEPTION_FORWARD_DECLARATION'.format(
            self.params.beautiful_capi_namespace.upper())
        with WatchdogScope(out, watchdog_string):
            out.put_line('namespace ' + self.params.beautiful_capi_namespace)
            with IndentScope(out):
                out.put_line(
                    'inline void check_and_throw_exception(int exception_code, void* exception_object);'
                )

    def generate_check_and_throw_exception(self, file_cache: FileCache):
        out = file_cache.get_file_for_check_and_throw_exception()
        out.put_begin_cpp_comments(self.params)
        with WatchdogScope(out,
                           self.params.beautiful_capi_namespace.upper() + '_CHECK_AND_THROW_EXCEPTION_INCLUDED'):
            with IfDefScope(out, '__cplusplus'):
                out.put_include_files()
                out.include_system_header('stdexcept')
                out.include_system_header('cassert')
                for exception_class in self.exception_classes:
                    out.include_user_header(
                        file_cache.class_header(exception_class.full_name_array))
                out.put_line('namespace {0}'.format(self.params.beautiful_capi_namespace))
                with IndentScope(out):
                    out.put_line(
                        'inline void check_and_throw_exception(int exception_code, void* exception_object)')
                    with IndentScope(out):
                        out.put_line('switch (exception_code)')
                        with IndentScope(out):
                            out.put_line('case 0:')
                            with Indent(out):
                                out.put_line('return;')
                            code_to_exception = {exception_class.exception_code: exception_class for exception_class
                                                 in self.exception_classes}
                            for code, exception_class in code_to_exception.items():
                                out.put_line('case {0}:'.format(code))
                                with Indent(out):
                                    out.put_line('throw {0}(exception_object, false);'.format(
                                        exception_class.full_wrap_name))
                            out.put_line('default:')
                            with Indent(out):
                                out.put_line('assert(false);')
                            out.put_line('case -1:')
                            with Indent(out):
                                out.put_line('throw std::runtime_error("unknown exception");')

    def generate_c_call(self, out: FileGenerator, return_type: ClassTypeGenerator or BuiltinTypeGenerator,
                        c_function_name: str, arguments: [str]) -> str:
        out.put_line('{0} exception_info;'.format(self.__exception_info_t()))
        arguments.insert(0, '&exception_info')
        c_function_call = '{function_name}({arguments})'.format(
            function_name=c_function_name,
            arguments=', '.join(arguments)
        )
        casting_instructions, return_expression = return_type.c_2_wrap_var('result', c_function_call)
        out.put_lines(casting_instructions)
        out.put_line('{0}::check_and_throw_exception(exception_info.code, exception_info.object_pointer);'.format(
            self.params.beautiful_capi_namespace))
        return return_expression

    def modify_c_arguments(self, arguments: [str]):
        arguments.insert(0, '{0}* exception_info'.format(self.__exception_info_t()))

    def __remember_exception_class(self, class_generator: ClassGenerator):
        if class_generator.class_object.exception and class_generator not in self.exception_classes:
            for derived_class_generator in class_generator.derived_class_generators:
                self.__remember_exception_class(derived_class_generator)
            self.exception_classes.append(class_generator)

    def __remember_exception_classes_for_namespace(self, namespace_generator: NamespaceGenerator):
        for nested_namespace_generator in namespace_generator.nested_namespaces:
            self.__remember_exception_classes_for_namespace(nested_namespace_generator)
        for class_generator in namespace_generator.classes:
            self.__remember_exception_class(class_generator)

    def __remember_exception_classes(self):
        if not self.exception_classes_generated:
            self.exception_classes_generated = True
            for root_namespace_generator in self.root_namespace_generators:
                self.__remember_exception_classes_for_namespace(root_namespace_generator)

    @staticmethod
    def __generate_catch_by_value(out: FileGenerator, exception_class_generator: ClassGenerator):
        out.put_line('catch (const {0}& exception_object)'.format(
            exception_class_generator.class_object.implementation_class_name
        ))
        with IndentScope(out):
            out.put_line('if (exception_info)')
            with IndentScope(out):
                out.put_line('exception_info->code = {0};'.format(exception_class_generator.exception_code))
                # TODO: Add exception handling here
                out.put_line('// TODO: Add exception handling here')
                out.put_line('exception_info->object_pointer = new {0}(exception_object);'.format(
                    exception_class_generator.class_object.implementation_class_name
                ))

    @staticmethod
    def __generate_catch_by_pointer(out: FileGenerator, exception_class_generator: ClassGenerator):
        out.put_line('catch ({0}* exception_object)'.format(
            exception_class_generator.class_object.implementation_class_name
        ))
        with IndentScope(out):
            out.put_line('if (exception_info)')
            with IndentScope(out):
                out.put_line('exception_info->code = {0};'.format(exception_class_generator.exception_code))
                out.put_line('exception_info->object_pointer = exception_object;')

    @staticmethod
    def __generate_catch(out: FileGenerator, exception_class_generator: ClassGenerator):
        ByFirstArgument.__generate_catch_by_value(out, exception_class_generator)
        ByFirstArgument.__generate_catch_by_pointer(out, exception_class_generator)

    def generate_implementation_call(
            self, out: FileGenerator, return_type: ClassTypeGenerator or BuiltinTypeGenerator, methods_calls: [str]):
        self.__remember_exception_classes()
        out.put_line('try')
        with IndentScope(out):
            out.put_line('if (exception_info)')
            with IndentScope(out):
                out.put_line('exception_info->code = 0;')
                out.put_line('exception_info->object_pointer = 0;')
            for method_call in methods_calls:
                out.put_line(method_call)
        for exception_class_generator in self.exception_classes:
            ByFirstArgument.__generate_catch(out, exception_class_generator)
        out.put_line('catch (...)')
        with IndentScope(out):
            out.put_line('if (exception_info)')
            with IndentScope(out):
                out.put_line('exception_info->code = -1;')
                out.put_line('exception_info->object_pointer = 0;')
        return_type.generate_c_default_return_value(out)

    def include_dependent_implementation_headers(self, file_generator: FileGenerator):
        for exception_class_generator in self.exception_classes:
            if exception_class_generator.class_object.implementation_class_header_filled:
                file_generator.include_user_header(exception_class_generator.class_object.implementation_class_header)
