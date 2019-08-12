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


from ClassGenerator import ClassGenerator
from NamespaceGenerator import NamespaceGenerator
from FileGenerator import FileGenerator, Indent
from ParamsParser import TBeautifulCapiParams
import posixpath

def replace_xml_scopes(line: str) -> str:
    return line.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '').replace('&gt;&gt;', '&gt; &gt;')

class NatvisGenerator(object):
    def __init__(self, namespace_generators: [NamespaceGenerator], params: TBeautifulCapiParams):
        self.namespace_generators = namespace_generators
        self.params = params

    def process_class(self, class_generator: ClassGenerator, out: FileGenerator, is_shared: bool):
        impl_name = replace_xml_scopes(class_generator.implementation_name)
        wrap_name = class_generator.full_wrap_name.replace('<', '&lt;').replace('>', '&gt;')
        out.put_line('<Type Name="{}">'.format(wrap_name))
        with Indent(out):
            out.put_line('<DisplayString>{{mObject = {mObject}}}</DisplayString>')
            out.put_line('<Expand>')
            with Indent(out):
                if is_shared:
                    out.put_line('<ExpandedItem>({0}.dll!{1}*)mObject</ExpandedItem>'.format(
                        self.params.shared_library_name, impl_name))
                else:
                    out.put_line('<ExpandedItem>({0}*)mObject</ExpandedItem>'.format(impl_name))
            out.put_line('</Expand>')
        out.put_line('</Type>')

    def process_namespace(self, namespace_generator: NamespaceGenerator, out: FileGenerator, is_shared: bool):
        for nested_namespace in namespace_generator.nested_namespaces:
            self.process_namespace(nested_namespace, out, is_shared)
        for class_generator in namespace_generator.classes:
            self.process_class(class_generator, out, is_shared)

    def generate(self, filename: str):
        start, ext = posixpath.splitext(filename)
        shared_name = filename
        static_name = start + '_static' + ext

        shared_out = FileGenerator(shared_name)
        shared_out.put_line('<?xml version="1.0" encoding="utf-8"?>')
        shared_out.put_line('<AutoVisualizer xmlns="http://schemas.microsoft.com/vstudio/debugger/natvis/2010">')
        with Indent(shared_out):
            for namespace_generator in self.namespace_generators:
                self.process_namespace(namespace_generator, shared_out, True)
        shared_out.put_line('</AutoVisualizer>')

        static_out = FileGenerator(static_name)
        static_out.put_line('<?xml version="1.0" encoding="utf-8"?>')
        static_out.put_line('<AutoVisualizer xmlns="http://schemas.microsoft.com/vstudio/debugger/natvis/2010">')
        with Indent(static_out):
            for namespace_generator in self.namespace_generators:
                self.process_namespace(namespace_generator, static_out, False)
        static_out.put_line('</AutoVisualizer>')
