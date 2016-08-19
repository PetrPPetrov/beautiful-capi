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

project(down_cast)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

SET(SWIG_DIR "/Users/Shared/Libraries/swig-3.0.10-install/")
SET(SWIG_EXECUTABLE "/Users/Shared/Libraries/swig-3.0.10-install/bin/swig")
include(../../example.cmake)
include(../../swig_example.cmake)

add_capi_generation()
add_swig_generation(swig DownCast)
include_directories(${down_cast_SOURCE_DIR}/source/)

add_library(down_cast SHARED
  ${down_cast_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${down_cast_SOURCE_DIR}/source/IShape.h
  ${down_cast_SOURCE_DIR}/source/IPolygon.h
  ${down_cast_SOURCE_DIR}/source/RefCountedImpl.h
  ${down_cast_SOURCE_DIR}/source/TriangleImpl.h
  ${down_cast_SOURCE_DIR}/source/TriangleImpl.cpp
  ${down_cast_SOURCE_DIR}/source/SquareImpl.h
  ${down_cast_SOURCE_DIR}/source/SquareImpl.cpp
  ${down_cast_SOURCE_DIR}/source/CircleImpl.h
  ${down_cast_SOURCE_DIR}/source/CircleImpl.cpp
  ${down_cast_SOURCE_DIR}/source/TriangleFactory.h
  ${down_cast_SOURCE_DIR}/source/TriangleFactory.cpp
  ${down_cast_SOURCE_DIR}/source/SquareFactory.h
  ${down_cast_SOURCE_DIR}/source/SquareFactory.cpp
  ${down_cast_SOURCE_DIR}/source/CircleFactory.h
  ${down_cast_SOURCE_DIR}/source/CircleFactory.cpp
)

add_cs_api_generation(cs DownCast)

setup_swig_module(swig DownCast)
add_swig_python(swig DownCast)
add_swig_csharp(swig DownCast)
