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

include(../../../UseBCapi.cmake)
add_bcapi_generation(sharp "sharp_output")

include(${down_cast_SOURCE_DIR}/source/AutoGenSourcesList.cmake)

include_directories(${down_cast_SOURCE_DIR}/source/)

add_library(down_cast SHARED
  ${DownCastAutoGenSources}
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

if(${CSHARP_ENABLED})
    add_subdirectory(sharp_output)
endif()
