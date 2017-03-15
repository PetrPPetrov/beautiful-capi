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

project(overload_suffix_client)

cmake_minimum_required(VERSION 2.8)

include_directories(${overload_suffix_client_SOURCE_DIR}/../library/include)

add_executable(overload_suffix_client
  ${overload_suffix_client_SOURCE_DIR}/Main.cpp
)

if(TARGET overload_suffix)
  add_dependencies(overload_suffix_client overload_suffix)
endif()
target_link_libraries(overload_suffix_client overload_suffix)
