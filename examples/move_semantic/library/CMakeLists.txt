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

project(move_semantic)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp)

add_custom_command(
  OUTPUT ${move_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${move_semantic_SOURCE_DIR}/../../../source/Main.py -i ${move_semantic_SOURCE_DIR}/move_semantic.xml -p ${move_semantic_SOURCE_DIR}/move_semantic_params.xml -o ${move_semantic_SOURCE_DIR}/include  -w ${move_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${move_semantic_SOURCE_DIR}/move_semantic.xml
  DEPENDS ${move_semantic_SOURCE_DIR}/move_semantic_params.xml
  WORKING_DIRECTORY ${move_semantic_SOURCE_DIR}
)

include_directories(${move_semantic_SOURCE_DIR}/source/)

add_library(move_semantic SHARED
  ${move_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${move_semantic_SOURCE_DIR}/source/PrinterImpl.h
  ${move_semantic_SOURCE_DIR}/source/PrinterImpl.cpp
)
