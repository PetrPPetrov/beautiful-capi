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

project(hello_world)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

SET(SWIG_DIR "/Users/Shared/Libraries/swig-3.0.10-install/")
SET(SWIG_EXECUTABLE "/Users/Shared/Libraries/swig-3.0.10-install/bin/swig")
include(../../example.cmake)
include(../../swig_example.cmake)

add_capi_generation()
add_swig_generation(swig HelloWorld)

include_directories(${hello_world_SOURCE_DIR}/source/)

add_library(hello_world SHARED
  ${hello_world_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${hello_world_SOURCE_DIR}/source/PrinterImpl.h
  ${hello_world_SOURCE_DIR}/source/PrinterImpl.cpp
)


setup_swig_module(swig HelloWorld)
add_swig_python(swig HelloWorld)
add_swig_csharp(swig HelloWorld)