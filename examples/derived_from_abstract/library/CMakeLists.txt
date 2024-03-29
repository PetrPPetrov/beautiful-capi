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

project(derived_from_abstract)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.6 REQUIRED)

include(../../../UseBCapi.cmake)
add_bcapi_generation(sharp "sharp_output")

include(${derived_from_abstract_SOURCE_DIR}/source/AutoGenSourcesList.cmake)

include_directories(${derived_from_abstract_SOURCE_DIR}/source/)

add_library(derived_from_abstract SHARED
  ${AutoGenSources}
  ${derived_from_abstract_SOURCE_DIR}/source/AnimalImpl.h
  ${derived_from_abstract_SOURCE_DIR}/source/BirdImpl.cpp
  ${derived_from_abstract_SOURCE_DIR}/source/BirdImpl.h
  ${derived_from_abstract_SOURCE_DIR}/source/WolfImpl.cpp
  ${derived_from_abstract_SOURCE_DIR}/source/WolfImpl.h
)

if(${CSHARP_ENABLED})
 add_subdirectory(sharp_output)
endif()
