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

find_package(PythonInterp)

add_custom_command(
  OUTPUT ${hello_world_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${hello_world_SOURCE_DIR}/../../../source/Main.py -i ${hello_world_SOURCE_DIR}/hello_world.xml -p ${hello_world_SOURCE_DIR}/hello_world_params.xml -o ${hello_world_SOURCE_DIR}/include -w ${hello_world_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${hello_world_SOURCE_DIR}/hello_world.xml
  DEPENDS ${hello_world_SOURCE_DIR}/hello_world_params.xml
  WORKING_DIRECTORY ${hello_world_SOURCE_DIR}
)

include_directories(${hello_world_SOURCE_DIR}/source/)

add_library(hello_world SHARED
  ${hello_world_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${hello_world_SOURCE_DIR}/source/PrinterImpl.h
  ${hello_world_SOURCE_DIR}/source/PrinterImpl.cpp
)
