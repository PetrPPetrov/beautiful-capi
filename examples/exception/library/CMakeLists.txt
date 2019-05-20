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

project(exception)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

include(../../../UseBCapi.cmake)
add_bcapi_generation()

include(${exception_SOURCE_DIR}/source/AutoGenSourcesList.cmake)

include_directories(${exception_SOURCE_DIR}/source/)

add_library(exception SHARED
  ${AutoGenSources}
  ${exception_SOURCE_DIR}/source/PrinterImpl.h
  ${exception_SOURCE_DIR}/source/PrinterImpl.cpp
  ${exception_SOURCE_DIR}/source/ScannerImpl.h
  ${exception_SOURCE_DIR}/source/ScannerImpl.cpp
  ${exception_SOURCE_DIR}/source/Exception/GenericImpl.h
  ${exception_SOURCE_DIR}/source/Exception/GenericImpl.cpp
  ${exception_SOURCE_DIR}/source/Exception/BadArgumentImpl.h
  ${exception_SOURCE_DIR}/source/Exception/BadArgumentImpl.cpp
  ${exception_SOURCE_DIR}/source/Exception/NullArgumentImpl.h
  ${exception_SOURCE_DIR}/source/Exception/NullArgumentImpl.cpp
  ${exception_SOURCE_DIR}/source/Exception/DivisionByZeroImpl.h
  ${exception_SOURCE_DIR}/source/Exception/DivisionByZeroImpl.cpp
)
