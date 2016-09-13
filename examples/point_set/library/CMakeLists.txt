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


project(point_set)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

include(../../../UseBCapi.cmake)

include_directories(
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/core/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/config/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/assert/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/throw_exception/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/predef/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/smart_ptr/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/type_traits/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/static_assert/include/
  ${point_set_SOURCE_DIR}/../../../3rdparty/boost/align/include/
  ${point_set_SOURCE_DIR}/source/
)

add_library(point_set SHARED
  ${point_set_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${point_set_SOURCE_DIR}/source/PointSetImpl.h
  ${point_set_SOURCE_DIR}/source/PointsImpl.h
  ${point_set_SOURCE_DIR}/source/PositionImpl.h
)

add_bcapi_generation()
