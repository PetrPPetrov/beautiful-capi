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

project(mixed_semantic)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

include(../../../UseBCapi.cmake)

include_directories(
  ${mixed_semantic_SOURCE_DIR}/source/
)

add_library(mixed_semantic SHARED
  ${mixed_semantic_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${mixed_semantic_SOURCE_DIR}/source/NameImpl.h
  ${mixed_semantic_SOURCE_DIR}/source/PersonImpl.h
  ${mixed_semantic_SOURCE_DIR}/source/AddressImpl.h
  ${mixed_semantic_SOURCE_DIR}/source/PrinterImpl.h
  
)

add_bcapi_generation(sharp "sharp_output")

if(${CSHARP_ENABLED} AND EXISTS ${mixed_semantic_SOURCE_DIR}/sharp_output)
    add_subdirectory(sharp_output)
endif()
