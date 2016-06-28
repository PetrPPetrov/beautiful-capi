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

import argparse
import os
from collections import OrderedDict

import Parser
import ParamsParser
from FileGenerator import FileGenerator, Indent, IndentScope
from Helpers import get_return_copy_or_add_ref


def get_class_type(type_name: str, api_description: Parser.TBeautifulCapiRoot):
    path_to_class = type_name.split('::')
    return __get_class_type_impl(path_to_class, api_description.m_namespaces)

def __get_class_type_impl(path_to_class, classes_or_namespaces):
    for class_or_namespace in classes_or_namespaces:
        if class_or_namespace.m_name == path_to_class[0]:
            if len(path_to_class) == 1:
                return class_or_namespace
            elif len(path_to_class) == 2:
                return __get_class_type_impl(path_to_class[1:], class_or_namespace.m_classes)
            else:
                return __get_class_type_impl(path_to_class[1:], class_or_namespace.m_namespaces)
    return None


class Description(object):
    def __init__(self, input_xml: str, input_params: str):
        from xml.dom.minidom import parse
        self.params = ParamsParser.load(parse(input_params))
        self.api = Parser.load(parse(input_xml))
        #process_beautiful_capi_root(self.api, self)


class Module(object):
    def __init__(self, name: str, description: Description, root_folder: str):
        self.name = name
        self.description = description
        self.root_folder = root_folder

    def generate(self):
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)

        module_file = FileGenerator(os.path.join(self.root_folder, self.name + '.i'))
        module_file.copyright_header = self.description.params.m_copyright_header
        module_file.automatic_generation_warning = self.description.params.m_automatic_generated_warning

        module_file.put_line('%module(directors="1", allprotected="1") {module_name}'.format(module_name=self.name))
        module_file.put_line('//enable namespace support')
        module_file.put_line('#if defined(SWIGCSHARP) || defined(SWIGJAVA)')
        module_file.put_line('    %nspace;')
        module_file.put_line('#endif')
        module_file.put_line('//hide all classes and function')
        module_file.put_line('%rename($ignore, %$isclass) "";')
        module_file.put_line('%rename($ignore, %$isfunction, %$not %$ismember) "";')
        module_file.put_line('')
        module_file.put_line('')

        module_file.put_line('%define %downcast(NAME, DERIVED, BASE)')
        module_file.put_line('%rename("%s") NAME;')
        module_file.put_line('%{')
        module_file.put_line('inline DERIVED* NAME(BASE* input_object)')
        module_file.put_line('{')
        module_file.put_line('    return dynamic_cast<DERIVED*>(input_object);')
        module_file.put_line('}')
        module_file.put_line('%}')
        module_file.put_line('inline DERIVED* NAME(BASE* input_object)')
        module_file.put_line('{')
        module_file.put_line('    return dynamic_cast<DERIVED*>(input_object);')
        module_file.put_line('}')
        module_file.put_line('%enddef')

        module_file.put_line('')
        module_file.put_line('//include namespaces')

        for namespace in self.description.api.m_namespaces:
            module_file.put_line('%include {namespace}.swg'.format(namespace=namespace.m_name))
            Namespace(namespace, self.description, self.root_folder).generate()


class Namespace(object):
    def __init__(self, namespace: Parser.TNamespace, description: Description, root_folder: str):
        self.namespace = namespace
        self.description = description
        self.root_folder = root_folder

    def generate(self):
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)

        namespace_file = FileGenerator(os.path.join(self.root_folder, self.namespace.m_name + '.swg'))

        namespace_file.copyright_header = self.description.params.m_copyright_header
        namespace_file.automatic_generation_warning = self.description.params.m_automatic_generated_warning

        headers = OrderedDict()
        for element in self.namespace.m_classes + self.namespace.m_functions:
            if isinstance(element, Parser.TClass):
                header = element.m_implementation_class_header
            elif isinstance(element, Parser.TFunction) and element.m_implementation_header_filled:
                header = element.m_implementation_header

            if header:
                if header not in headers.keys():
                    headers[header] = list()
                headers[header].append(element)

        namespace_file.put_line('%{')
        for header in headers.keys():
            namespace_file.put_line('    #include "{header}"'.format(header=header))
        namespace_file.put_line('%}')
        namespace_file.put_line('')

        for header in headers.keys():
            for element in headers[header]:
                namespace_file.put_line('')
                if isinstance(element, Parser.TClass):
                    self.generate_class(element, namespace_file)
                elif isinstance(element, Parser.TFunction):
                    self.generate_function(element, namespace_file)

            namespace_file.put_line('%include "{header}"'.format(header=header))

        for namespace in self.namespace.m_namespaces:
            namespace_file.put_line('%include {current}/{child}.swg'.format(current=self.namespace.m_name,
                                                                            child=namespace.m_name))
            Namespace(namespace, self.description, os.path.join(self.root_folder, namespace.m_name)).generate()

    def generate_class(self, element: Parser.TClass, swig_file: FileGenerator):
        nspaces = element.m_implementation_class_name.split('::')
        impl_name = nspaces.pop(-1)

        swig_file.put_line('%rename("{iface}", %$isclass) {impl};'.format(iface=element.m_name, impl=impl_name))
        swig_file.put_line('%feature("director") {impl};'.format(impl=impl_name))

        if element.m_pointer_access_filled and element.m_pointer_access:

            nspace_decls = ['namespace ' + n for n in nspaces]
            nspace_open = ' { '.join(nspace_decls + [' '])
            nspace_close = '} ' * len(nspaces)

            swig_file.put_line(nspace_open)

            with Indent(swig_file):
                swig_file.put_line('class {impl} {{}};'.format(impl=impl_name))
                swig_file.put_line('%extend {impl}'.format(impl=impl_name))
                with IndentScope(swig_file):

                    for constructor in element.m_constructors:
                        arg_names = [arg.m_name for arg in constructor.m_arguments]
                        arg_desc = [arg.m_type + ' ' + arg.m_name for arg in constructor.m_arguments]

                        swig_file.put_line('{impl}({args})'.format(impl=impl_name, args=', '.join(arg_desc)))
                        with IndentScope(swig_file):
                            swig_file.put_line('return new {full_name}({args});'.format(full_name=element.m_implementation_class_name, args=', '.join(arg_names)))

                    for method in element.m_methods:
                        arg_names = [arg.m_name for arg in method.m_arguments]
                        arg_desc = [arg.m_type + ' ' + arg.m_name for arg in method.m_arguments]

                        swig_file.put_line('{ret} {name}({args})'.format(ret=method.m_return if method.m_return else 'void', name=method.m_name, args=', '.join(arg_desc)))
                        with IndentScope(swig_file):
                            line = '$self->operator->()->{name}({args});'.format(name=method.m_name, args=', '.join(arg_names))
                            if method.m_return_filled and method.m_return is not 'void':
                                line = 'return ' + line
                            swig_file.put_line(line)
            swig_file.put_line(nspace_close)
            swig_file.put_line('%rename($ignore, %$isclass) {impl};'.format(iface=element.m_name, impl=impl_name))
        else:
            if element.m_lifecycle == Parser.TLifecycle.reference_counted:
                swig_file.put_line('%feature("ref")   {impl} "$this->AddRef();"'.format(impl=impl_name))
                swig_file.put_line('%feature("unref") {impl} "$this->Release();"'.format(impl=impl_name))
            if element.m_lifecycle != Parser.TLifecycle.raw_pointer_semantic:
                leaky = filter(lambda m: get_return_copy_or_add_ref(m), element.m_methods)
                for method in leaky:
                    # TODO: may need to fully specify method parameters
                    swig_file.put_line('%newobject {impl}::{method};'.format(impl=impl_name, method=method.m_name))

        if element.m_base_filled:
            base_type = get_class_type(element.m_base, self.description.api)
            while base_type:
                swig_file.put_line('%downcast({base}_to_{impl}, {full_impl}, {full_base})'.format(
                    full_impl=element.m_implementation_class_name, full_base=base_type.m_implementation_class_name,
                    impl=impl_name, base=base_type.m_implementation_class_name.split('::')[-1]))

                base_type = get_class_type(base_type.m_base, self.description.api)

    @staticmethod
    def generate_function(function: Parser.TFunction, swig_file: FileGenerator):
        impl_name = function.m_implementation_name.split('::')[-1]
        swig_file.put_line(
            '%rename("{iface}", %$isfunction, %$not %$ismember) {impl};'.format(iface=function.m_name, impl=impl_name))
        if get_return_copy_or_add_ref(function):
            swig_file.put_line('%newobject {impl};'.format(impl=impl_name))


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi Swig',
        description='This program generates Swig wrappers for your C++ classes.')

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
        '-m', '--module-name', nargs=None, default='', metavar='MODULE_NAME',
        help='specifies module name for wrapper')

    args = parser.parse_args()

    description = Description(args.input, args.params)
    module = Module(args.module_name, description, args.output_folder)
    module.generate()

main()
