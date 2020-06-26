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
from Helpers import get_full_method_name


class OverloadSuffixesProcessor(object):
    def __init__(self, root_node: TBeautifulCapiRoot):
        self.root_node = root_node
        self.cur_overload_suffix_mode = TOverloadSuffixMode.Off
        self.namespace_stack = []

    class ParamsScope(object):
        def __init__(self, overload_suffixes_processor, namespace_or_class: TNamespace or TClass):
            self.overload_suffixes_processor = overload_suffixes_processor
            self.old_overload_suffix_mode = self.overload_suffixes_processor.cur_overload_suffix_mode
            if namespace_or_class.overload_suffix_mode_filled:
                self.overload_suffixes_processor.cur_overload_suffix_mode = namespace_or_class.overload_suffix_mode
            self.overload_suffixes_processor.namespace_stack.append(namespace_or_class.name)

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.overload_suffixes_processor.namespace_stack.pop()
            self.overload_suffixes_processor.cur_overload_suffix_mode = self.old_overload_suffix_mode

    def __check_for_unique(self, routines: [object]):
        if self.cur_overload_suffix_mode != TOverloadSuffixMode.Off:
            existing_names = {}
            for routine in routines:
                name = ''.join(get_full_method_name(routine))
                if name in existing_names:
                    existing_names[name] += 1
                    old_suffix = routine.overload_suffix
                    routine.overload_suffix += str(existing_names[name])
                    if self.cur_overload_suffix_mode == TOverloadSuffixMode.Notify:
                        print(
                            'Warning: Method or function {routine_name}() is overloaded'
                            ' and has no unique overload suffix ("{old_suffix}"). '
                            'Suffix "{suffix}" has been installed.'.format(
                                routine_name='::'.join(self.namespace_stack) + '::' + routine.name,
                                old_suffix=old_suffix,
                                suffix=routine.overload_suffix))
                else:
                    existing_names[name] = 0

    def __process_class(self, cur_class: TClass):
        with OverloadSuffixesProcessor.ParamsScope(self, cur_class):
            self.__check_for_unique(cur_class.methods)
            self.__check_for_unique(cur_class.indexers)

    def __process_namespace(self, namespace: TNamespace):
        with OverloadSuffixesProcessor.ParamsScope(self, namespace):
            self.__check_for_unique(namespace.functions)
            for nested_namespace in namespace.namespaces:
                self.__process_namespace(nested_namespace)
            for cur_class in namespace.classes:
                self.__process_class(cur_class)

    def process(self):
        for cur_namespace in self.root_node.namespaces:
            self.cur_overload_suffix_mode = cur_namespace.overload_suffix_mode
            self.__process_namespace(cur_namespace)


def process(root_node: TBeautifulCapiRoot):
    suffixes_processor = OverloadSuffixesProcessor(root_node)
    suffixes_processor.process()
