#!/usr/bin/env python
#
# Software Package: Beautiful C-API
# Copyright holder: Petr Petrovich Petrov
#
# Description: A source-code wrapping tool which automates
# the creation of compiler-independent and binary compatible C++ libraries
# across different C++ compilers, written in Python 3,
# using XML format API descriptions as input.
#
# Hosted on public source-code site github
# https://github.com/PetrPPetrov/beautiful-capi/
# Default Public license: GNU General Public License Version 3
#
# This license agreement is between the parties with Effective Date: 1st February 2018:
# Licensor: Petr Petrovich Petrov, and
# Licensee: Visual Technology Services Ltd.
#
# This agreement creates a private,
# confidential license between the licensee and licensor,
# separate and distinct from the default public license.
#
# The license grants full commercial use,
# including the rights to modify, extend,
# create derivative works, package, distribute,
# and sub-license to 3rd parties.
#
# This license shall survive any changes
# to the public software or license,
# including if the public license is changed
# or the software is deleted, lost or withdrawn.
#
# The license grants rights of the licensee
# to pass this license on to a successor organization
# in the event of source-code escrow release
# or company change of ownership.
#
# The licensor remains owner and copyright holder
# and shall be acknowledged in documentation copyright notices.
# The license is permanent and remains in effect indefinitely,
# unless modified by a further written agreement.


from ClassGenerator import ClassGenerator
from NamespaceGenerator import NamespaceGenerator
from FileGenerator import FileGenerator, Indent
from ParamsParser import TBeautifulCapiParams


class NatvisGenerator(object):
    def __init__(self, namespace_generators: [NamespaceGenerator], params: TBeautifulCapiParams):
        self.namespace_generators = namespace_generators
        self.params = params

    def process_class(self, class_generator: ClassGenerator, out: FileGenerator):
        impl_name = class_generator.implementation_name.replace('<', '&lt;').replace('>', '&gt;')
        wrap_name = class_generator.full_wrap_name.replace('<', '&lt;').replace('>', '&gt;')
        out.put_line('<Type Name="{}">'.format(wrap_name))
        with Indent(out):
            out.put_line('<DisplayString> mObject </DisplayString>')
            out.put_line('<Expand>')
            with Indent(out):
                out.put_line('<ExpandedItem>({0}.dll!{1}*)mObject</ExpandedItem>'.format(
                    self.params.shared_library_name, impl_name))
            out.put_line('</Expand>')
        out.put_line('</Type>')

    def process_namespace(self, namespace_generator: NamespaceGenerator, out: FileGenerator):
        for nested_namespace in namespace_generator.nested_namespaces:
            self.process_namespace(nested_namespace, out)
        for class_generator in namespace_generator.classes:
            self.process_class(class_generator, out)

    def generate(self, filename: str):
        out = FileGenerator(filename)
        out.put_line('<?xml version="1.0" encoding="utf-8"?>')
        out.put_line('<AutoVisualizer xmlns="http://schemas.microsoft.com/vstudio/debugger/natvis/2010">')
        with Indent(out):
            for namespace_generator in self.namespace_generators:
                self.process_namespace(namespace_generator, out)
        out.put_line('</AutoVisualizer>')
