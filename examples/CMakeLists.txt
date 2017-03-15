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

project(examples)

cmake_minimum_required(VERSION 2.8)

add_subdirectory(boost_shared_ptr)
add_subdirectory(callback)
add_subdirectory(circular_reference)
add_subdirectory(clanguage)
add_subdirectory(copy_semantic)
add_subdirectory(custom_suffix)
add_subdirectory(down_cast)
add_subdirectory(exception)
add_subdirectory(hello_world)
add_subdirectory(object_parameter)
add_subdirectory(overload_suffix)
add_subdirectory(point_set)
add_subdirectory(raw_pointer_semantic)
add_subdirectory(reference_counted)
add_subdirectory(template)
add_subdirectory(unit_test)
add_subdirectory(virtual_interface)
