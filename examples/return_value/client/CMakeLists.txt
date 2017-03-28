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

project(return_value_client)

cmake_minimum_required(VERSION 2.8)

find_package(Boost)

if(NOT WIN32)
  add_definitions(-fvisibility=default)
endif()

include_directories(
  ${Boost_INCLUDE_DIR}/
  ${return_value_client_SOURCE_DIR}/../library/include
  ${return_value_client_SOURCE_DIR}/
)

add_executable(return_value_client
  ${return_value_client_SOURCE_DIR}/Main.cpp
)

if(TARGET point_set)
  add_dependencies(return_value_client return_value)
endif()
target_link_libraries(return_value_client return_value)
