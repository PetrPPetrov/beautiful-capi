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


class DynamicLoad(CfunctionTraitsBase):
    def __init__(self, capi_generator):
        super().__init__(capi_generator)


def create_loader_traits(dynamically_load_functions, capi_generator):
    if dynamically_load_functions:
        return DynamicLoad(capi_generator)
    else:
        return ImplLib(capi_generator)
