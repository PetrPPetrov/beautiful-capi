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

project(external_class_client)

cmake_minimum_required(VERSION 2.8)

include_directories(
  ${external_class_client_SOURCE_DIR}/
  ${classes_SOURCE_DIR}/include
  ${components_SOURCE_DIR}/include
  ${comp_c_SOURCE_DIR}/include
  ${printer_SOURCE_DIR}/include
)

add_executable(external_class_client
  ${external_class_client_SOURCE_DIR}/Main.cpp
)

if(TARGET classes)
  add_dependencies(external_class_client classes)
endif()
if(TARGET components)
  add_dependencies(external_class_client components)
endif()
if(TARGET component)
  add_dependencies(external_class_client comp_c)
endif()
if(TARGET printer)
  add_dependencies(external_class_client printer)
endif()

target_link_libraries(external_class_client classes)
target_link_libraries(external_class_client components)
target_link_libraries(external_class_client comp_c)
target_link_libraries(external_class_client printer)
