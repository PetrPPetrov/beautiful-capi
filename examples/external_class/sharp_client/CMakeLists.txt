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

project(external_class_sharp_client LANGUAGES CSharp)
cmake_minimum_required(VERSION 3.8.2)

add_executable(external_class_sharp_client
  ${external_class_sharp_client_SOURCE_DIR}/Program.cs
  ${external_class_sharp_client_SOURCE_DIR}/Properties/AssemblyInfo.cs
)

SET_TARGET_PROPERTIES(external_class_sharp_client PROPERTIES LINKER_LANGUAGE CSharp)
if(TARGET classes_sharp_library)
    add_dependencies(external_class_sharp_client classes_sharp_library)
endif()
if(TARGET components_sharp_library)
    add_dependencies(external_class_sharp_client components_sharp_library)
endif()
if(TARGET component_sharp_library)
    add_dependencies(external_class_sharp_client comp_c_sharp_library)
endif()
if(TARGET printer_sharp_library)
    add_dependencies(external_class_sharp_client printer_sharp_library)
endif()

target_link_libraries(external_class_sharp_client printer_sharp_library comp_c_sharp_library components_sharp_library classes_sharp_library)
