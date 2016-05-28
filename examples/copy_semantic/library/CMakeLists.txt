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

project(copy_semantic)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

add_custom_command(
  OUTPUT ${copy_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${copy_semantic_SOURCE_DIR}/../../../source/Main.py -i ${copy_semantic_SOURCE_DIR}/copy_semantic.xml -p ${copy_semantic_SOURCE_DIR}/copy_semantic_params.xml -o ${copy_semantic_SOURCE_DIR}/include -w ${copy_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${copy_semantic_SOURCE_DIR}/copy_semantic.xml
  DEPENDS ${copy_semantic_SOURCE_DIR}/copy_semantic_params.xml
  WORKING_DIRECTORY ${copy_semantic_SOURCE_DIR}
)

include_directories(${copy_semantic_SOURCE_DIR}/source/)

add_library(copy_semantic SHARED
  ${copy_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${copy_semantic_SOURCE_DIR}/source/PrinterImpl.h
  ${copy_semantic_SOURCE_DIR}/source/PrinterImpl.cpp
)
