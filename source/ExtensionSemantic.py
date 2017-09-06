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


from copy import deepcopy

from Parser import TClass, TNamespace, TBeautifulCapiRoot


class ExtensionSemanticProcessor(object):
    def __init__(self, root_node: TBeautifulCapiRoot):
        self.root_node = root_node
        self.class_stack = []

    def process_class(self, cur_class: TClass, cur_namespace: TNamespace):
        self.class_stack.append(cur_class.name)
        for lifecycle_extension in cur_class.lifecycle_extensions:
            new_extension_class = deepcopy(cur_class)
            new_extension_class.name = lifecycle_extension.name
            new_extension_class.lifecycle = lifecycle_extension.lifecycle
            new_extension_class.lifecycle_filled = True
            new_extension_class.wrap_name = lifecycle_extension.wrap_name
            new_extension_class.wrap_name_filled = lifecycle_extension.wrap_name_filled
            new_extension_class.cast_tos = deepcopy(lifecycle_extension.cast_tos)
            new_extension_class.lifecycle_extensions = []
            new_extension_class.lifecycle_extension = lifecycle_extension
            new_extension_class.extension_base_class_name = '::'.join(self.class_stack)
            new_extension_class.down_cast = lifecycle_extension.down_cast
            new_extension_class.down_cast_filled = True

            cur_namespace.classes.append(new_extension_class)
        self.class_stack.pop()

    def process_namespace(self, namespace: TNamespace):
        self.class_stack.append(namespace.name)
        for nested_namespace in namespace.namespaces:
            self.process_namespace(nested_namespace)
        for cur_class in namespace.classes:
            self.process_class(cur_class, namespace)
        self.class_stack.pop()

    def process(self):
        for cur_namespace in self.root_node.namespaces:
            self.process_namespace(cur_namespace)


def process(root_node: TBeautifulCapiRoot):
    semantic_processor = ExtensionSemanticProcessor(root_node)
    semantic_processor.process()
