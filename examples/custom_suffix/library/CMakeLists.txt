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

project(custom_suffix)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

include(../../../UseBCapi.cmake)

include_directories(${custom_suffix_SOURCE_DIR}/source/)

add_library(custom_suffix SHARED
  ${custom_suffix_SOURCE_DIR}/source/auto_gen_wrap.cpp
  ${custom_suffix_SOURCE_DIR}/source/printer_impl.h
  ${custom_suffix_SOURCE_DIR}/source/printer_impl.cpp
  ${custom_suffix_SOURCE_DIR}/source/scanner_impl.h
  ${custom_suffix_SOURCE_DIR}/source/scanner_impl.cpp
  ${custom_suffix_SOURCE_DIR}/source/plotter_impl.h
  ${custom_suffix_SOURCE_DIR}/source/plotter_impl.cpp
)

add_bcapi_generation(wrap ${custom_suffix_SOURCE_DIR}/source/auto_gen_wrap.cpp)
