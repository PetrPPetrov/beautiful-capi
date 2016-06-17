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

import FileGenerator
from LifecycleTraits import CreateLifecycleTraits


def generate_down_casts_for_class(output_file, cur_class, capi_generator):
    if cur_class.m_base:
        pass
    else:
        output_file.put_line('/* {0} does not have any base type */'.format(cur_class.m_name))


def generate_down_casts_for_namespace(output_file, namespace, capi_generator):
    output_file.put_line('')
    output_file.put_line('namespace {0}'.format(namespace.m_name))
    with FileGenerator.IndentScope(output_file):
        for cur_class in namespace.m_classes:
            with CreateLifecycleTraits(cur_class, capi_generator):
                generate_down_casts_for_class(output_file, cur_class, capi_generator)
        for nested_namespace in namespace.m_namespaces:
            generate_down_casts_for_namespace(output_file, nested_namespace, capi_generator)
