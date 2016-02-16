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

project(ref_counted)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp)

add_custom_command(
  OUTPUT ${ref_counted_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${ref_counted_SOURCE_DIR}/../../../source/Main.py -i ${ref_counted_SOURCE_DIR}/ref_counted.xml -p ${ref_counted_SOURCE_DIR}/ref_counted_params.xml -o ${ref_counted_SOURCE_DIR}/include  -w ${ref_counted_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${ref_counted_SOURCE_DIR}/ref_counted.xml
  DEPENDS ${ref_counted_SOURCE_DIR}/ref_counted_params.xml
  WORKING_DIRECTORY ${ref_counted_SOURCE_DIR}
)

include_directories(${ref_counted_SOURCE_DIR}/source/)

add_library(ref_counted SHARED
  ${ref_counted_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${ref_counted_SOURCE_DIR}/source/PrinterImpl.h
  ${ref_counted_SOURCE_DIR}/source/PrinterImpl.cpp
)
