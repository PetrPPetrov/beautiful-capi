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


from Parser import TExternalEnumeration


class ExternalEnumGenerator(object):
    def __init__(self, enum_object: TExternalEnumeration, parent_generator):
        self.enum_object = enum_object
        self.parent_generator = parent_generator

    @property
    def name(self) -> str:
        return self.enum_object.name

    @property
    def wrap_name(self) -> str:
        return self.name

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_generator.full_wrap_name, self.name]) if self.parent_generator else self.name

    @property
    def full_wrap_name(self) -> str:
        return self.full_name

    @property
    def implementation_name(self) -> str:
            return self.full_wrap_name
