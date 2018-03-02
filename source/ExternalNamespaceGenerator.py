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


from Parser import TExternalNamespace


class ExternalNamespaceGenerator(object):
    def __init__(self, namespace_object: TExternalNamespace, parent_namespace):
        self.namespace_object = namespace_object
        self.parent_namespace = parent_namespace
        self.nested_namespaces = []
        self.classes = []
        self.enum_generators = []

    @property
    def name(self) -> str:
        return self.namespace_object.name

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_namespace.full_name, self.name]) if self.parent_namespace else self.name

    @property
    def full_name_array(self) -> [str]:
        return self.parent_namespace.full_name_array + [self.name] if self.parent_namespace else [self.name]

    @property
    def wrap_name(self) -> str:
        return self.name

