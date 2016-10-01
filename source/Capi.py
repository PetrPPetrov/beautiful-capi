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
import shutil
import argparse
import ExceptionTraits
from xml.dom.minidom import parse
from Helpers import BeautifulCapiException
from CreateGenerators import create_namespace_generators
from FileCache import FileCache
from CapiGenerator import CapiGenerator
from Templates import process as process_templates
from Callbacks import process as process_callbacks
from ParamsParser import TBeautifulCapiParams, TExceptionHandlingMode, load
from ParseRoot import parse_root


class Capi(object):
    def __init__(self,
                 input_filename,
                 input_params_filename,
                 output_folder,
                 output_wrap_file_name,
                 internal_snippets_folder,
                 clean):
        self.input_xml = input_filename
        self.input_params = parse(input_params_filename)
        self.output_folder = output_folder
        self.output_wrap_file_name = output_wrap_file_name
        self.internal_snippets_folder = internal_snippets_folder
        self.api_description = None
        self.params_description = None
        if clean:
            if os.path.exists(self.output_folder):
                shutil.rmtree(self.output_folder)
            if os.path.exists(self.internal_snippets_folder):
                shutil.rmtree(self.internal_snippets_folder)

    def substitute_project_name(self, params: TBeautifulCapiParams):
        if not self.api_description.project_name:
            raise BeautifulCapiException('project_name parameter is not specified')
        params.check_and_throw_exception_filename = params.check_and_throw_exception_filename.format(
            project_name=self.api_description.project_name
        )
        params.beautiful_capi_namespace = params.beautiful_capi_namespace.format(
            project_name=self.api_description.project_name)
        autogen_prefix_template = params.autogen_prefix_for_internal_callback_implementation
        params.autogen_prefix_for_internal_callback_implementation = autogen_prefix_template.format(
            project_name=self.api_description.project_name)
        params.root_header = params.root_header.format(
            project_name=self.api_description.project_name)

    def generate(self):
        self.params_description = load(self.input_params)
        self.params_description.output_folder = self.output_folder
        self.params_description.internal_snippets_folder = self.internal_snippets_folder
        self.params_description.output_wrap_file_name = self.output_wrap_file_name
        self.api_description = parse_root(self.input_xml)
        self.substitute_project_name(self.params_description)

        process_templates(self.api_description)
        first_namespace_generators = create_namespace_generators(
            self.api_description, self.params_description)

        process_callbacks(first_namespace_generators)
        namespace_generators = create_namespace_generators(
            self.api_description, self.params_description)

        by_first_argument_exception_traits = ExceptionTraits.ByFirstArgument(
                self.params_description, namespace_generators)
        no_handling_exception_traits = ExceptionTraits.NoHandling()
        if self.params_description.exception_handling_mode == TExceptionHandlingMode.by_first_argument:
            main_exception_traits = by_first_argument_exception_traits
        else:
            main_exception_traits = no_handling_exception_traits

        capi_generator = CapiGenerator(main_exception_traits, no_handling_exception_traits)
        file_cache = FileCache(self.params_description)
        for namespace_generator in namespace_generators:
            namespace_generator.generate(file_cache, capi_generator)

        capi_generator.generate(file_cache, self.params_description)


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
        '-i', '--input', nargs=None, default='input.xml', metavar='INPUT',
        help='specifies input API description file')
    parser.add_argument(
        '-p', '--params', nargs=None, default='params.xml', metavar='PARAMS',
        help='specifies wrapper generation parameters input file')
    parser.add_argument(
        '-o', '--output-folder', nargs=None, default='./output', metavar='OUTPUT_FOLDER',
        help='specifies output folder for generated files')
    parser.add_argument(
        '-w', '--output-wrap-file-name', nargs=None, default='./capi_wrappers.cpp', metavar='OUTPUT_WRAP',
        help='specifies output file name for wrapper C-functions')
    parser.add_argument(
        '-s', '--internal-snippets-folder', nargs=None, default='./internal_snippets', metavar='OUTPUT_SNIPPETS',
        help='specifies output folder for generated library snippets')
    parser.add_argument(
        '-c', '--clean', nargs=None, default=False, metavar='CLEAN',
        help='specifies whether if clean input and snippets directories'
    )

    args = parser.parse_args()

    capi = Capi(
        args.input,
        args.params,
        args.output_folder,
        args.output_wrap_file_name,
        args.internal_snippets_folder,
        args.clean
    )
    capi.generate()

if __name__ == '__main__':
    main()
