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

from Constants import Constants
from TraitsBase import TraitsBase


class CfunctionTraitsBase(TraitsBase):
    def __init__(self, capi_generator):
        super().__init__(None, capi_generator)


class ImplLib(CfunctionTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)

    def __put_define_apple_or_linux(self):
        self.put_line('#define {0} extern "C"'.format(self.capi_generator.cur_api_define))

    def generate_c_functions_declarations(self):
        self.capi_generator.cur_api_define = '{0}_API'.format(self.capi_generator.get_namespace_id().upper())
        self.put_line('#ifdef _WIN32')
        with self.indent():
            self.put_line('#define {0} extern "C" __declspec(dllimport)'.format(self.capi_generator.cur_api_define))
        self.put_line('#elif __APPLE__')
        with self.indent():
            self.__put_define_apple_or_linux()
        self.put_line('#elif __unix__ || __linux__')
        with self.indent():
            self.__put_define_apple_or_linux()
        self.put_line('#else')
        with self.indent():
            self.put_line('#error "Unknown platform"')
        self.put_line('#endif')
        self.capi_generator.api_defines_generated = True


class DynamicLoad(CfunctionTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)

    def generate_c_functions_declarations(self):
        pass


def create_loader_traits(dynamically_load_functions, capi_generator):
    if dynamically_load_functions:
        return DynamicLoad(capi_generator)
    else:
        return ImplLib(capi_generator)
