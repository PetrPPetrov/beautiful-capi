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


from FileGenerator import FileGenerator
from FileCache import FileCache


class ThisArgumentGenerator(object):
    def __init__(self, class_argument_generator):
        from ArgumentGenerator import ClassTypeGenerator
        self.type_generator = ClassTypeGenerator(class_argument_generator)

    def wrap_2_c(self) -> str:
        return '{get_raw_pointer_method}()'.format(
            get_raw_pointer_method=self.type_generator.class_argument_generator.params.get_raw_pointer_method_name)

    @staticmethod
    def c_argument_declaration() -> str:
        return 'void* object_pointer'

    def c_2_implementation(self) -> str:
        return self.type_generator.c_2_implementation_pointer('object_pointer')

    @staticmethod
    def implementation_2_c() -> str:
        return 'mObject'

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass
