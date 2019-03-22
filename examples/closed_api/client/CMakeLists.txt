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

project(closed_api_client)

cmake_minimum_required(VERSION 2.8)

include_directories(
    ${closed_api_client_SOURCE_DIR}/../library/include
    ${closed_api_client_SOURCE_DIR}/../library/keys
)

add_executable(closed_api_client
  ${closed_api_client_SOURCE_DIR}/Main.cpp
)

if(TARGET closed_api)
  add_dependencies(closed_api_client closed_api)
endif()
target_link_libraries(closed_api_client closed_api)
