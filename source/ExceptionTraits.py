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


import ParamsParser
import FileGenerator
from TraitsBase import TraitsBase
from FileGenerator import NewFileScope
from FileGenerator import WatchdogScope
from FileGenerator import IndentScope
from FileGenerator import IfDefScope
from FileGenerator import Indent


class ExceptionTraitsBase(TraitsBase):
    def __init__(self, cur_method, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)
        self.cur_method = cur_method


class NoHandling(ExceptionTraitsBase):
    def __init__(self, cur_method, cur_class, capi_generator):
        super().__init__(cur_method, cur_class, capi_generator)

    def generate_codes(self):
        pass

    def generate_check_and_throw_exception_header(self):
        pass

    def generate_check_and_throw_exception_forward_declaration(self):
        pass

    def generate_exception_info(self):
        pass

    def generate_check_and_throw_exception_callback(self):
        pass

    def include_check_and_throw_exception_header(self):
        pass

    def generate_implementation_call(self, method_call, return_type):
        cur_file = self.capi_generator.output_source
        cur_file.put_line(method_call)

    def generate_implementation_callback(self, method_call, return_type):
        self.generate_implementation_call(method_call, return_type)

    def generate_c_call(self, c_method_name, format_string, is_function):
        cur_file = self.capi_generator.output_header
        self.capi_generator.put_raw_pointer_structure_if_required(cur_file, self.cur_method.arguments)
        cur_file.put_line(self.capi_generator.get_wrapped_return_instruction(
            self.cur_method.return_type if hasattr(self.cur_method, 'return_type') else '',
            format_string.format(
                c_function=c_method_name,
                arguments=', '.join(self.get_c_from_wrapped_arguments_for_function() if is_function
                                    else self.get_c_from_wrapped_arguments())
            ),
            self.cur_method
        ))

    def get_c_from_wrapped_arguments(self):
        return self.capi_generator.get_c_from_wrapped_arguments_impl(self.cur_method.arguments)

    def get_c_from_wrapped_arguments_for_function(self):
        return self.capi_generator.get_c_from_wrapped_arguments_for_function_impl(self.cur_method.arguments)

    def get_c_argument_pairs(self):
        return self.capi_generator.get_c_argument_pairs_impl(self.cur_method.arguments)

    def get_c_argument_pairs_for_function(self):
        return self.capi_generator.get_c_argument_pairs_for_function_impl(self.cur_method.arguments)


class ByFirstArgument(ExceptionTraitsBase):
    def __init__(self, cur_method, cur_class, capi_generator):
        super().__init__(cur_method, cur_class, capi_generator)
        self.additional_includes = None
        self.current_exception_index = 1

    def __generate_codes_for_class(self, cur_class):
        if cur_class.exception:
            self.capi_generator.exception_class_2_code.update({cur_class: self.current_exception_index})
            self.current_exception_index += 1

    def __generate_codes_for_namespace(self, namespace):
        for cur_class in namespace.classes:
            self.__generate_codes_for_class(cur_class)
        for nested_namespace in namespace.namespaces:
            self.__generate_codes_for_namespace(nested_namespace)

    def __process_class(self, cur_class):
        if cur_class.exception:
            cur_file = self.capi_generator.output_header
            cur_file.put_line(
                'case {0}:'.format(self.capi_generator.exception_class_2_code[cur_class])
            )
            self.current_exception_index += 1
            cur_class_extra_info = self.capi_generator.extra_info[cur_class]
            with NewFileScope(self.additional_includes, self.capi_generator):
                self.capi_generator.file_traits.include_class_header(
                    cur_class_extra_info.full_name_array[:-1],
                    cur_class
                )
            with Indent(cur_file):
                cur_file.put_line('throw {0}(exception_object, false);'.format(cur_class_extra_info.get_class_name()))

    def __process_namespace(self, namespace):
        for cur_class in namespace.classes:
            self.__process_class(cur_class)
        for nested_namespace in namespace.namespaces:
            self.__process_namespace(nested_namespace)

    def __generate_check_and_throw_exception(self):
        cur_file = self.capi_generator.output_header
        cur_file.put_line('inline void check_and_throw_exception(int exception_code, void* exception_object)')
        with IndentScope(cur_file):
            cur_file.put_line('switch (exception_code)')
            with IndentScope(cur_file):
                cur_file.put_line('case 0:')
                with Indent(cur_file):
                    cur_file.put_line('return;')
                for cur_namespace in self.capi_generator.api_description.namespaces:
                    self.__process_namespace(cur_namespace)
                cur_file.put_line('default:')
                with Indent(cur_file):
                    cur_file.put_line('assert(false);')
                cur_file.put_line('case -1:')
                with Indent(cur_file):
                    cur_file.put_line('throw std::runtime_error("unknown exception");')

    # TODO: avoid copy-paste from __process_class() method
    def __process_callback(self, cur_class):
        if cur_class.exception:
            cur_file = self.capi_generator.output_header
            cur_file.put_line(
                'case {0}:'.format(self.capi_generator.exception_class_2_code[cur_class])
            )
            with Indent(cur_file):
                with IndentScope(cur_file):
                    cur_file.put_line('{0}* impl_exception_object = static_cast<{0}*>(exception_object);'.format(
                        cur_class.implementation_class_name
                    ))
                    cur_file.put_line('{0} saved_exception_object = *impl_exception_object;'.format(
                        cur_class.implementation_class_name
                    ))
                    cur_file.put_line('delete impl_exception_object;')
                    cur_file.put_line('throw saved_exception_object;')

    # TODO: avoid copy-paste from __process_namespace() method
    def __process_namespace_callback(self, namespace):
        for cur_class in namespace.classes:
            self.__process_callback(cur_class)
        for nested_namespace in namespace.namespaces:
            self.__process_namespace_callback(nested_namespace)

    # TODO: avoid copy-paste from __generate_check_and_throw_exception() method
    def generate_check_and_throw_exception_callback(self):
        cur_file = self.capi_generator.output_header
        cur_file.put_line('inline void check_and_throw_exception(int exception_code, void* exception_object)')
        with IndentScope(cur_file):
            cur_file.put_line('switch (exception_code)')
            with IndentScope(cur_file):
                cur_file.put_line('case 0:')
                with Indent(cur_file):
                    cur_file.put_line('return;')
                for cur_namespace in self.capi_generator.api_description.namespaces:
                    self.__process_namespace_callback(cur_namespace)
                cur_file.put_line('default:')
                with Indent(cur_file):
                    cur_file.put_line('assert(false);')
                cur_file.put_line('case -1:')
                with Indent(cur_file):
                    cur_file.put_line('throw std::runtime_error("unknown exception");')

    def generate_codes(self):
        for cur_namespace in self.capi_generator.api_description.namespaces:
            self.__generate_codes_for_namespace(cur_namespace)

    def generate_check_and_throw_exception_header(self):
        with NewFileScope(
            self.capi_generator.file_traits.get_file_for_check_and_throw_exception(), self.capi_generator
        ):
            cur_file = self.capi_generator.output_header
            cur_file.put_begin_cpp_comments(self.capi_generator.params_description)
            with WatchdogScope(cur_file, 'BEAUTIFUL_CAPI_CHECK_AND_THROW_EXCEPTION_INCLUDED'):
                with IfDefScope(cur_file, '__cplusplus'):
                    cur_file.put_line('#include <stdexcept>')
                    cur_file.put_line('#include <cassert>')
                    self.additional_includes = FileGenerator.FileGenerator(None)
                    cur_file.put_file(self.additional_includes)
                    cur_file.put_line('')
                    cur_file.put_line('namespace beautiful_capi')
                    with IndentScope(cur_file):
                        self.__generate_check_and_throw_exception()

    def generate_check_and_throw_exception_forward_declaration(self):
        cur_file = self.capi_generator.output_header
        cur_file.put_begin_cpp_comments(self.capi_generator.params_description)
        with WatchdogScope(cur_file, 'BEAUTIFUL_CAPI_CHECK_AND_THROW_EXCEPTION_FORWARD_DECLARATION'):
                cur_file.put_line('namespace beautiful_capi')
                with IndentScope(cur_file):
                    cur_file.put_line(
                        'inline void check_and_throw_exception(int exception_code, void* exception_object);'
                    )

    @staticmethod
    def generate_exception_info_impl(cur_file):
        with WatchdogScope(cur_file, 'BEAUTIFUL_CAPI_EXCEPTION_INFO_DEFINED'):
            cur_file.put_line('struct beautiful_capi_exception_info_t')
            with IndentScope(cur_file, '};'):
                cur_file.put_line('int code;')
                cur_file.put_line('void* object_pointer;')

    def generate_exception_info(self):
        ByFirstArgument.generate_exception_info_impl(self.capi_generator.output_header)
        ByFirstArgument.generate_exception_info_impl(self.capi_generator.output_source)

    def include_check_and_throw_exception_header(self):
        self.capi_generator.file_traits.include_check_and_throw_exception_header()

    def __generate_catch_for_class_by_value(self, cur_exception_class):
        cur_file = self.capi_generator.output_source
        cur_file.put_line(
            'catch (const {0}& exception_object)'.format(cur_exception_class.implementation_class_name)
        )
        with IndentScope(cur_file):
            cur_file.put_line('if (exception_info)')
            with IndentScope(cur_file):
                cur_file.put_line('exception_info->code = {0};'.format(
                    self.capi_generator.exception_class_2_code[cur_exception_class])
                )
                cur_file.put_line('exception_info->object_pointer = new {0}(exception_object);'.format(
                    cur_exception_class.implementation_class_name
                ))

    def __generate_catch_for_class_by_pointer(self, cur_exception_class):
        cur_file = self.capi_generator.output_source
        cur_file.put_line(
            'catch ({0}* exception_object)'.format(cur_exception_class.implementation_class_name)
        )
        with IndentScope(cur_file):
            cur_file.put_line('if (exception_info)')
            with IndentScope(cur_file):
                cur_file.put_line('exception_info->code = {0};'.format(
                    self.capi_generator.exception_class_2_code[cur_exception_class])
                )
                cur_file.put_line('exception_info->object_pointer = exception_object;')

    def __generate_catch_for_callback_by_value(self, cur_exception_class):
        cur_exception_extra_info = self.capi_generator.extra_info[cur_exception_class]
        cur_file = self.capi_generator.output_source
        cur_file.put_line(
            'catch ({0}& exception_object)'.format(
                cur_exception_extra_info.get_class_name())
        )
        with IndentScope(cur_file):
            cur_file.put_line('if (exception_info)')
            with IndentScope(cur_file):
                cur_file.put_line('exception_info->code = {0};'.format(
                    self.capi_generator.exception_class_2_code[cur_exception_class])
                )
                cur_file.put_line('exception_info->object_pointer = exception_object.Detach();')

    def __generate_catch_for_class(self, cur_exception_class):
        for derived_exception_class in self.capi_generator.extra_info[cur_exception_class].derived_objects:
            self.__generate_catch_for_class(derived_exception_class)
        self.capi_generator.loader_traits.add_impl_header(cur_exception_class.implementation_class_header)
        self.__generate_catch_for_class_by_value(cur_exception_class)
        self.__generate_catch_for_class_by_pointer(cur_exception_class)

    def __generate_catch_for_callback(self, cur_exception_class):
        for derived_exception_class in self.capi_generator.extra_info[cur_exception_class].derived_objects:
            self.__generate_catch_for_callback(derived_exception_class)
        self.__generate_catch_for_callback_by_value(cur_exception_class)

    def __generate_implementation_call(self, method_call, return_type, catch_generator):
        cur_file = self.capi_generator.output_source
        cur_file.put_line('try')
        with IndentScope(cur_file):
            cur_file.put_line('if (exception_info)')
            with IndentScope(cur_file):
                cur_file.put_line('exception_info->code = 0;')
                cur_file.put_line('exception_info->object_pointer = 0;')
            cur_file.put_line(method_call)
        for cur_exception_class in self.capi_generator.exception_class_2_code:
            if not cur_exception_class.base:
                catch_generator(self, cur_exception_class)
        cur_file.put_line('catch (...)')
        with IndentScope(cur_file):
            cur_file.put_line('if (exception_info)')
            with IndentScope(cur_file):
                cur_file.put_line('exception_info->code = -1;')
                cur_file.put_line('exception_info->object_pointer = 0;')
        if return_type:
            cur_file.put_line('return static_cast<{0}>(0);'.format(self.capi_generator.get_c_type(return_type)))

    def generate_implementation_call(self, method_call, return_type):
        self.__generate_implementation_call(method_call, return_type, ByFirstArgument.__generate_catch_for_class)

    def generate_implementation_callback(self, method_call, return_type):
        self.__generate_implementation_call(method_call, return_type, ByFirstArgument.__generate_catch_for_callback)

    def generate_c_call(self, c_method_name, format_string, is_function):
        cur_file = self.capi_generator.output_header
        self.capi_generator.put_raw_pointer_structure_if_required(cur_file, self.cur_method.arguments)
        cur_file.put_line('beautiful_capi_exception_info_t exception_info;')
        cur_file.put_line(self.capi_generator.get_wrapped_result_var(
            self.cur_method.return_type if hasattr(self.cur_method, 'return_type') else '',
            format_string.format(
                c_function=c_method_name,
                arguments=', '.join(self.get_c_from_wrapped_arguments_for_function() if is_function
                                    else self.get_c_from_wrapped_arguments())
            ),
            self.cur_method
        ))
        cur_file.put_line(
            'beautiful_capi::check_and_throw_exception(exception_info.code, exception_info.object_pointer);'
        )
        if hasattr(self.cur_method, 'return_type') and self.cur_method.return_type:
            cur_file.put_line('return result;')

    @staticmethod
    def get_c_from_wrapped():
        return ['&exception_info']

    def get_c_from_wrapped_arguments(self):
        return ByFirstArgument.get_c_from_wrapped() + \
               self.capi_generator.get_c_from_wrapped_arguments_impl(self.cur_method.arguments)

    def get_c_from_wrapped_arguments_for_function(self):
        return ByFirstArgument.get_c_from_wrapped() + \
               self.capi_generator.get_c_from_wrapped_arguments_for_function_impl(self.cur_method.arguments)

    @staticmethod
    def get_c_argument():
        return ['beautiful_capi_exception_info_t* exception_info']

    def get_c_argument_pairs(self):
        return ByFirstArgument.get_c_argument() + \
               self.capi_generator.get_c_argument_pairs_impl(self.cur_method.arguments)

    def get_c_argument_pairs_for_function(self):
        return ByFirstArgument.get_c_argument() + \
               self.capi_generator.get_c_argument_pairs_for_function_impl(self.cur_method.arguments)


str_to_exception_traits = {
    ParamsParser.TExceptionHandlingMode.no_handling: NoHandling,
    ParamsParser.TExceptionHandlingMode.by_first_argument: ByFirstArgument
}


def create_exception_traits(cur_method, cur_class, capi_generator):
    if cur_method.noexcept:
        return NoHandling(cur_method, cur_class, capi_generator)
    if capi_generator.params_description.exception_handling_mode in str_to_exception_traits:
        return str_to_exception_traits[capi_generator.params_description.exception_handling_mode](
            cur_method, cur_class, capi_generator
        )
    raise ValueError


class CreateExceptionTraits(object):
    def __init__(self, cur_method, cur_class, capi_generator):
        self.cur_method = cur_method
        self.cur_class = cur_class
        self.capi_generator = capi_generator
        self.previous_exception_traits = capi_generator.exception_traits

    def __enter__(self):
        self.capi_generator.exception_traits = create_exception_traits(
            self.cur_method, self.cur_class, self.capi_generator
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capi_generator.exception_traits = self.previous_exception_traits
