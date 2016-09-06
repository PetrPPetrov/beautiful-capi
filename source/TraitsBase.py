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


class TraitsBase(object):
    def __init__(self, cur_class, capi_generator):
        self.cur_class = cur_class
        self.capi_generator = capi_generator
        try:
            self.cur_extra_info = None
            if cur_class:
                self.cur_extra_info = capi_generator.extra_info[cur_class]
            self.cur_base_extra_info = None
            if self.cur_class and self.cur_class.base:
                base_class_type = capi_generator.get_class_type(self.cur_class.base)
                if base_class_type:
                    self.cur_base_extra_info = self.capi_generator.extra_info[base_class_type]
        except:
            pass

    def put_line(self, line, eol='\n'):
        self.capi_generator.output_header.put_line(line, eol)

    def put_file(self, another_file):
        self.capi_generator.output_header.put_file(another_file)

    def put_source_line(self, line, eol='\n'):
        self.capi_generator.output_source.put_line(line, eol)

    def put_source_file(self, another_file):
        self.capi_generator.output_source.put_file(another_file)

    def indent(self):
        return FileGenerator.Indent(self.capi_generator.output_header)

    def indent_scope(self):
        return FileGenerator.IndentScope(self.capi_generator.output_header)

    def indent_source(self):
        return FileGenerator.Indent(self.capi_generator.output_source)

    def indent_scope_source(self):
        return FileGenerator.IndentScope(self.capi_generator.output_source)

    def get_cur_class_short_name(self):
        return self.cur_extra_info.get_class_short_name()

    def get_cur_class_name(self):
        return self.cur_extra_info.get_class_name()

    def get_base_class_short_name(self):
        return self.cur_base_extra_info.get_class_short_name()

    def get_base_class_name(self):
        return self.cur_base_extra_info.get_class_name()
