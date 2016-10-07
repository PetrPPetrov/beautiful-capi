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


from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IfDefScope, IndentScope, Unindent
from CheckBinaryCompatibilityGenerator import generate_check_version


class StaticLoaderGenerator(object):
    def __init__(self, namespace_name, namespace_info, params: TBeautifulCapiParams):
        self.namespace_name = namespace_name
        self.namespace_info = namespace_info
        self.params = params

    def __generate_constructor(self, out: FileGenerator):
        out.put_line('Initialization()')
        with IndentScope(out):
            generate_check_version(
                out, self.namespace_info.namespace_name_array[0],
                '"{0}"'.format(self.params.shared_library_name) if self.params.shared_library_name else '')

    def __generate_body(self, out: FileGenerator):
        out.put_line('class Initialization')
        with IndentScope(out, '};'):
            with Unindent(out):
                out.put_line('public:')
            self.__generate_constructor(out)

    def generate(self, out: FileGenerator):
        out.put_line('')
        with IfDefScope(out, '__cplusplus'):
            out.put_line('#include <stdexcept>')
            out.put_line('#include <sstream>')
            out.put_line('')
            # We always have at least one element
            out.put_line('namespace {0}'.format(self.namespace_info.namespace_name_array[0]))
            with IndentScope(out):
                self.__generate_body(out)
