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
import sys
import copy
import shutil
import argparse
from xml.dom.minidom import parse

import ExceptionTraits
from Helpers import BeautifulCapiException, format_type
from CreateGenerators import create_namespace_generators
from FileCache import FileCache, full_relative_path_from_candidates
from CapiGenerator import CapiGenerator
from FileGenerator import FileGenerator, Indent, IndentScope, Unindent, WatchdogScope, IfDefScope
from NatvisGenerator import NatvisGenerator
from Templates import process as process_templates
from Callbacks import process as process_callbacks
from Properties import process as process_properties
from ExtensionSemantic import process as process_extension_semantic
from CheckBinaryCompatibilityGenerator import process as process_check_binary_compatibility
from ParamsParser import TBeautifulCapiParams, TExceptionHandlingMode, load
from ParseRoot import parse_root
from UnitTestGenerator import TestGenerator
from OverloadSuffixes import process as process_overload_suffixes
from EnumGenerator import process_enum_impl_functions
from Parser import TExternalNamespace, TExternalClass, TExternalEnumeration
from CSharp import generate as generate_sharp_code


class Capi(object):
    def __init__(self,
                 input_filename,
                 input_params_filename,
                 output_folder=None,
                 sharp_output_folder=None,
                 output_wrap_file_name=None,
                 internal_snippets_folder=None,
                 api_keys_folder=None,
                 clean=None,
                 unit_tests_file=None,
                 natvis_file=None,
                 verbosity=None,
                 open_api=None,
                 single_file_wrap=None
                 ):
        self.input_xml = input_filename
        self.input_params_filename = input_params_filename
        try:
            self.input_params = parse(input_params_filename)
        except Exception as error:
            print("XML API parameters parsing error, {0}".format(input_params_filename))
            for arg in error.args:
                print("{0}".format(arg))
            sys.exit(1)
        self.output_folder = output_folder
        self.sharp_output_folder = sharp_output_folder
        self.output_wrap_file_name = output_wrap_file_name
        self.internal_snippets_folder = internal_snippets_folder
        self.api_keys_folder = api_keys_folder
        self.api_description = None
        self.params_description = None
        self.unit_tests_file = unit_tests_file
        self.natvis_file = natvis_file
        self.external_libs_headers = []
        self.open_api = open_api
        self.single_file_wrap = single_file_wrap
        if clean:
            if os.path.exists(self.output_folder):
                shutil.rmtree(self.output_folder)
            if os.path.exists(self.internal_snippets_folder):
                shutil.rmtree(self.internal_snippets_folder)
            if os.path.exists(self.sharp_output_folder):
                shutil.rmtree(self.sharp_output_folder)
        self.verbosity = verbosity
        self.unit_tests_generator = None

    def __substitute_project_name(self, params: TBeautifulCapiParams):
        if not self.api_description.project_name:
            raise BeautifulCapiException('project_name parameter is not specified')
        params.check_and_throw_exception_filename = params.check_and_throw_exception_filename.format(
            project_name=self.api_description.project_name
        )
        params.beautiful_capi_namespace = params.beautiful_capi_namespace.format(
            project_name=self.api_description.project_name)
        autogen_prefix_template = params.autogen_prefix_for_internal_implementation
        params.autogen_prefix_for_internal_implementation = autogen_prefix_template.format(
            project_name=self.api_description.project_name)
        params.root_header = params.root_header.format(
            project_name=self.api_description.project_name)

    def __generate_root_initializer(self, out: FileGenerator, namespace_generators: []):
        out.put_line('class {0}'.format(self.params_description.root_header_initializer))
        with IndentScope(out, '};'):
            member_names = []
            for namespace_generator in namespace_generators:
                member_name = namespace_generator.wrap_name.lower() + '_module_init'
                out.put_line('{namespace}::Initialization {member};'.format(
                    namespace=namespace_generator.wrap_name,
                    member=member_name))
                member_names.append(member_name)
            out.put_line('')
            if not self.params_description.shared_library_name:
                out.put_line('{0}();'.format(self.params_description.root_header_initializer))
            with Unindent(out):
                out.put_line('public:')
            if member_names:
                with IfDefScope(out, '{0}_LIBRARY_USE_DYNAMIC_LOADER'.format(
                        self.api_description.project_name.upper()), False):
                    out.put_line('{0}(const char* shared_library_name) :'.format(
                        self.params_description.root_header_initializer))
                    with Indent(out):
                        for member_name in member_names[:-1]:
                            out.put_line('{member_name}(shared_library_name),'.format(member_name=member_name))
                        out.put_line('{member_name}(shared_library_name)'.format(member_name=member_names[-1]))
                    with IndentScope(out):
                        pass
                if self.params_description.shared_library_name:
                    out.put_line('{0}()'.format(self.params_description.root_header_initializer))
                    with IndentScope(out):
                        pass

    def __generate_root_header(self, namespace_generators: [], file_cache: FileCache):
        if self.params_description.root_header and self.api_description.project_name:
            root_header = FileGenerator(os.path.join(self.output_folder, self.params_description.root_header))
            root_header.put_begin_cpp_comments(self.params_description)
            with WatchdogScope(root_header, self.api_description.project_name.upper() + '_LIBRARY_ROOT_INCLUDED'):
                with IfDefScope(root_header, '{0}_LIBRARY_USE_DYNAMIC_LOADER'.format(
                        self.api_description.project_name.upper()), False):
                    for namespace_generator in namespace_generators:
                        root_header.put_line('#define {0}_CAPI_USE_DYNAMIC_LOADER'.format(
                            namespace_generator.wrap_name.upper()))
                root_header.put_line('')

                with IfDefScope(root_header, '{0}_LIBRARY_DEFINE_FUNCTION_POINTERS'.format(
                        self.api_description.project_name.upper()), False):
                    for namespace_generator in namespace_generators:
                        root_header.put_line('#define {0}_CAPI_DEFINE_FUNCTION_POINTERS'.format(
                            namespace_generator.wrap_name.upper()))
                root_header.put_line('')

                root_header.put_include_files(False)
                for namespace_generator in namespace_generators:
                    root_header.include_user_header(file_cache.namespace_header(namespace_generator.full_name_array))
                if self.params_description.root_header_initializer:
                    root_header.put_line('')
                    with IfDefScope(root_header, '__cplusplus'):
                        if self.params_description.root_header_namespace:
                            root_header.put_line('namespace {0}'.format(self.params_description.root_header_namespace))
                            with IndentScope(root_header):
                                self.__generate_root_initializer(root_header, namespace_generators)
                        else:
                            self.__generate_root_initializer(root_header, namespace_generators)

    @staticmethod
    def __substitute_implementation_class_name(namespace):
        for sub_namespace in namespace.namespaces:
            Capi.__substitute_implementation_class_name(sub_namespace)
        for cur_class in namespace.classes:
            cur_class.implementation_class_name = format_type(cur_class.implementation_class_name)

    def __load_external(self, namespace):
        input_xml_folder = os.path.split(os.path.realpath(self.input_xml))[0]
        for external_lib in namespace.external_libraries:
            external_xml = full_relative_path_from_candidates(
                external_lib.input_xml_file, input_xml_folder, self.params_description.additional_include_directories)
            if self.params_description.verbosity:
                print('loading external library: {0}'.format(external_xml))
            external_params = full_relative_path_from_candidates(
                external_lib.params_xml_file, input_xml_folder, self.params_description.additional_include_directories)
            new_capi = Capi(external_xml, external_params, None, None, None, None, None, None, None)
            new_capi.params_description = load(new_capi.input_params)
            new_params = new_capi.params_description
            new_params.verbosity = self.params_description.verbosity
            new_capi.api_description = parse_root(new_capi.input_xml, new_params)
            new_capi.__substitute_project_name(new_capi.params_description)
            if external_lib.main_header:
                for define in external_lib.defines:
                    self.external_libs_headers.append(('define', define.value))
                self.external_libs_headers.append(('include', external_lib.main_header))
            if self.params_description.verbosity:
                print('loaded external library: {0}'.format(external_xml))

            def process_external_enum(enum, parent):
                file_cache = FileCache(new_params)
                external_enum = TExternalEnumeration()
                external_enum.name = enum.name
                external_enum.underlying_type = enum.enum_object.underlying_type
                external_enum.include_declaration = enum.declaration_header(file_cache)
                external_enum.include_definition = enum.definition_header(file_cache)
                parent.enumerations.append(external_enum)

            def process_external_namespaces(namespaces: [object], external_namespaces: [object]):
                for cur_namespace in namespaces:
                    external_namespace = TExternalNamespace()
                    external_namespace.name = cur_namespace.name
                    external_namespace.detach_method_name = new_params.detach_method_name
                    external_namespace.get_raw_pointer_method_name = new_params.get_raw_pointer_method_name
                    file_cache = FileCache(new_params)
                    external_namespace.include = file_cache.namespace_header(cur_namespace.full_name_array)
                    process_external_namespaces(cur_namespace.nested_namespaces, external_namespace.namespaces)
                    for cur_class in cur_namespace.classes:
                        external_class = TExternalClass()
                        external_class.name = cur_class.name
                        external_class.wrap_name = cur_class.wrap_name
                        external_class.include_declaration = file_cache.class_header_decl(cur_class.full_name_array)
                        external_class.include_definition = file_cache.class_header(cur_class.full_name_array)
                        external_namespace.classes.append(external_class)
                        for enum in cur_class.enum_generators:
                            process_external_enum(enum, external_class)
                        if cur_class.class_object.typedef_name:
                            external_class2 = copy.deepcopy(external_class)
                            external_class2.name = cur_class.class_object.typedef_name
                            external_namespace.classes.append(external_class2)
                    for enum in cur_namespace.enum_generators:
                        process_external_enum(enum, external_namespace)
                    external_namespaces.append(external_namespace)
            process_external_namespaces(new_capi.__process(), namespace.external_namespaces)
            if namespace.external_namespaces:
                namespace.external_namespaces[-1].project_name = new_capi.api_description.project_name
        for nested_namespace in namespace.namespaces:
            self.__load_external(nested_namespace)

    def __process(self) -> [object]:
        for namespace in self.api_description.namespaces:
            self.__load_external(namespace)
        process_check_binary_compatibility(self.api_description, self.params_description)
        process_overload_suffixes(self.api_description)
        process_templates(self.api_description)
        process_properties(self.api_description, self.unit_tests_generator)
        if self.unit_tests_generator:
            process_enum_impl_functions(self.api_description)
        process_extension_semantic(self.api_description)
        first_namespace_generators = create_namespace_generators(
            self.api_description, self.params_description)
        process_callbacks(first_namespace_generators)
        return first_namespace_generators

    def __generate(self):
        self.__process()
        for namespace in self.api_description.namespaces:
            Capi.__substitute_implementation_class_name(namespace)
        namespace_generators = create_namespace_generators(
            self.api_description, self.params_description)
        by_first_argument_exception_traits = ExceptionTraits.ByFirstArgument(
            self.params_description, namespace_generators)
        no_handling_exception_traits = ExceptionTraits.NoHandling()
        if self.params_description.exception_handling_mode == TExceptionHandlingMode.by_first_argument:
            main_exception_traits = by_first_argument_exception_traits
        else:
            main_exception_traits = no_handling_exception_traits
        capi_generator = CapiGenerator(main_exception_traits, no_handling_exception_traits,
                                       self.params_description, self.api_description)
        file_cache = FileCache(self.params_description)
        for namespace_generator in namespace_generators:
            namespace_generator.generate(file_cache, capi_generator)
        for command, value in self.external_libs_headers:
            if command == 'include':
                capi_generator.additional_includes.include_user_header(value)
            elif command == 'define':
                capi_generator.additional_defines.put_line('#define {0}'.format(value))

        capi_generator.generate(namespace_generators, file_cache)
        self.__generate_root_header(namespace_generators, file_cache)

        if self.unit_tests_generator:
            self.unit_tests_generator.generate(namespace_generators)

        if self.params_description.natvis_file_filled:
            if self.params_description.shared_library_name_filled:
                natvis_generator = NatvisGenerator(namespace_generators, self.params_description)
                filename = self.params_description.natvis_file
                if not os.path.isabs(filename):
                    filename = os.path.join(os.path.dirname(self.input_params_filename), filename)
                natvis_generator.generate(filename)
            else:
                print('Warning: To generate the natvis file, you must specify shared_library_name in the params file')

        if self.sharp_output_folder:
            if self.params_description.shared_library_name_filled:
                generate_sharp_code(file_cache, capi_generator, namespace_generators)
            else:
                print('Warning: To generate the C# code, you must specify shared_library_name in the params file')
        file_cache.file2generator.clear()

    def generate(self):
        self.params_description = load(self.input_params)
        self.params_description.verbosity = self.verbosity
        self.params_description.output_folder = self.output_folder
        self.params_description.sharp_output_folder = self.sharp_output_folder
        self.params_description.internal_snippets_folder = self.internal_snippets_folder
        self.params_description.api_keys_folder = self.api_keys_folder
        self.params_description.output_wrap_file_name = self.output_wrap_file_name
        if self.open_api is not None:
            self.params_description.open_api = self.open_api
            self.params_description.open_api_filled = True
        if self.natvis_file:
            self.params_description.natvis_file = self.natvis_file
            self.params_description.natvis_file_filled = True
        if self.single_file_wrap is not None:
            self.params_description.single_file_wrap = self.single_file_wrap
            self.params_description.single_file_wrap_filled = True
        if not self.params_description.open_api:
            self.params_description.single_file_wrap = True
            self.params_description.single_file_wrap_filled = True
        self.api_description = parse_root(self.input_xml, self.params_description)
        self.__substitute_project_name(self.params_description)

        if self.unit_tests_file:
            self.unit_tests_generator = TestGenerator(self.params_description, self.unit_tests_file)

        self.__generate()


def str2bool(value):
    lowercased = value.lower()
    if lowercased in ['true', '1']:
        return True
    elif lowercased in ['false', '0']:
        return False
    raise ValueError('Need bool; got %r' % value)


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi',
        description='This program generates C and C++ wrappers for your C++ classes.')

    parser.add_argument(
        '-i', '--input', nargs=None, dest='input',
        help='specifies input API description file')
    parser.add_argument(
        '-p', '--params', nargs=None, default='params.xml', dest='params',
        help='specifies generation parameters input file')
    parser.add_argument(
        '-o', '--output-folder', nargs=None, default='./output', dest='output_folder',
        help='specifies output folder for generated files')
    parser.add_argument(
        '-S', '--sharp-output-folder', nargs=None, default='', dest='sharp_output_folder',
        help='specifies output folder for generated files for C#')
    parser.add_argument(
        '-w', '--output-wrap-file-name', nargs=None, default='./capi_wrappers.cpp', dest='output_wrap',
        help='specifies output file name for wrapper C-functions')
    parser.add_argument(
        '-s', '--internal-snippets-folder', nargs=None, default='./internal_snippets', dest='output_snippets',
        help='specifies output folder for generated library snippets')
    parser.add_argument(
        '-k', '--api-keys-folder', nargs=None, default='./keys', dest='api_keys_folder',
        help='specifies output folder for generated API keys')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true',
                        help='cleans input, sharp output and snippets directories')
    parser.set_defaults(clean=False)
    parser.add_argument('-v', '--version', dest='version', action='store_true',
                        help='shows version number')
    parser.set_defaults(version=False)
    parser.add_argument('-t', '--tests-file', nargs=None, default="", dest='unit_tests_file',
                        help='generates unit tests for properties into specified file')
    parser.add_argument('-n', '--natvis-file', nargs=None, default="", dest='natvis_file',
                        help='generates .natvis file, specifies file name for .natvis file')
    parser.add_argument('--verbosity', dest='verbosity', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('--open-api', dest='open_api', type=str2bool, help='specifies flag if the library API will '
                        'be open, otherwise the library API will be secured.')
    parser.set_defaults(open_api=None)
    parser.add_argument('--single-file-wrap', dest='single_file_wrap', type=str2bool,
                        help='specifies flag to generate only one wrap file, even in open api mode.')
    parser.set_defaults(single_file_wrap=None)

    args = parser.parse_args()

    if args.version:
        print('Beautiful Capi version 0.4.\n')

    if args.verbosity:
        print("verbosity turned on")

    if not args.input:
        return

    capi = Capi(
        args.input,
        args.params,
        args.output_folder,
        args.sharp_output_folder,
        args.output_wrap,
        args.output_snippets,
        args.api_keys_folder,
        args.clean,
        args.unit_tests_file,
        args.natvis_file,
        args.verbosity,
        args.open_api,
        args.single_file_wrap
    )
    capi.generate()


if __name__ == '__main__':
    main()
