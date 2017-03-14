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


from Parser import TClass, TNamespace, TBeautifulCapiRoot, TOverloadSuffixMode


class OverloadSuffixesProcessor(object):
    def __init__(self, root_node: TBeautifulCapiRoot):
        self.root_node = root_node
        self.cur_overload_suffix_mode = TOverloadSuffixMode.Off
        self.namespace_stack = []

    def process_class(self, cur_class: TClass):
        old_overload_suffix_mode = self.cur_overload_suffix_mode
        if cur_class.overload_suffix_mode_filled:
            self.cur_overload_suffix_mode = cur_class.overload_suffix_mode
        self.namespace_stack.append(cur_class.name)
        if self.cur_overload_suffix_mode != TOverloadSuffixMode.Off:
            methods = {}
            for method in cur_class.methods:
                name = method.name + method.overload_suffix
                if name in methods:
                    methods[name] += 1
                    method.overload_suffix = str(methods[name])
                    if self.cur_overload_suffix_mode == TOverloadSuffixMode.Notify:
                        print(
                            'Warning: Method {method_name}() is overloaded and has no overload_suffix. '
                            'Default suffix "{suffix}" has been installed.'.format(
                                method_name='::'.join(self.namespace_stack) + '::' + method.name,
                                suffix=method.overload_suffix))
                else:
                    methods[name] = 0
        self.namespace_stack.pop()
        self.cur_overload_suffix_mode = old_overload_suffix_mode

    def process_namespace(self, namespace: TNamespace):
        old_overload_suffix_mode = self.cur_overload_suffix_mode
        if namespace.overload_suffix_mode_filled:
            self.cur_overload_suffix_mode = namespace.overload_suffix_mode
        self.namespace_stack.append(namespace.name)
        if self.cur_overload_suffix_mode != TOverloadSuffixMode.Off:
            functions = {}
            for function in namespace.functions:
                name = function.name + function.overload_suffix
                if name in functions:
                    functions[name] += 1
                    function.overload_suffix = str(functions[name])
                    if self.cur_overload_suffix_mode == TOverloadSuffixMode.Notify:
                        print(
                            'Warning: Function {full_name}() is overloaded and has no overload_suffix. '
                            'Default suffix "{suffix}" has been installed.'.format(
                                full_name='::'.join(self.namespace_stack) + '::' + name,
                                suffix=function.overload_suffix))
                else:
                    functions[name] = 0
        for nested_namespace in namespace.namespaces:
            self.process_namespace(nested_namespace)
        for cur_class in namespace.classes:
            self.process_class(cur_class)
        self.namespace_stack.pop()
        self.cur_overload_suffix_mode = old_overload_suffix_mode

    def process(self):
        for cur_namespace in self.root_node.namespaces:
            self.cur_overload_suffix_mode = cur_namespace.overload_suffix_mode
            self.process_namespace(cur_namespace)


def process(root_node: TBeautifulCapiRoot):
    suffixes_processor = OverloadSuffixesProcessor(root_node)
    suffixes_processor.process()
