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

project(template)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

include(../../example.cmake)
include(../../swig_example.cmake)

add_capi_generation()
add_swig_generation(swig Template)

include_directories(
  ${template_SOURCE_DIR}/../../../3rdparty/boost/core/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/config/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/assert/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/throw_exception/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/predef/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/smart_ptr/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/type_traits/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/static_assert/include/
  ${template_SOURCE_DIR}/../../../3rdparty/boost/align/include/
  ${template_SOURCE_DIR}/source/
)

add_library(template SHARED
  ${template_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${template_SOURCE_DIR}/source/VectorImpl.h
  ${template_SOURCE_DIR}/source/PositionImpl.h
  ${template_SOURCE_DIR}/source/ModelImpl.h
)

add_cs_api_generation(cs Template)

setup_swig_module(swig Template)
add_swig_python(swig Template)
add_swig_csharp(swig Template)
