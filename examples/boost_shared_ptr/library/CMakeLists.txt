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

project(boost_shared_ptr)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

SET(SWIG_DIR "/Users/Shared/Libraries/swig-3.0.10-install/")
SET(SWIG_EXECUTABLE "/Users/Shared/Libraries/swig-3.0.10-install/bin/swig")
include(../../example.cmake)
include(../../swig_example.cmake)

add_capi_generation()
add_swig_generation(swig BoostSharedPtr)

include_directories(
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/core/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/config/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/assert/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/throw_exception/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/predef/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/smart_ptr/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/type_traits/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/static_assert/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/align/include/
  ${boost_shared_ptr_SOURCE_DIR}/source/
)

add_library(boost_shared_ptr SHARED
  ${boost_shared_ptr_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${boost_shared_ptr_SOURCE_DIR}/source/PrinterImpl.h
  ${boost_shared_ptr_SOURCE_DIR}/source/PrinterImpl.cpp
)

add_cs_api_generation(cs BoostSharedPtr)

setup_swig_module(swig BoostSharedPtr)
add_swig_python(swig BoostSharedPtr)
add_swig_csharp(swig BoostSharedPtr)
