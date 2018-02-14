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

project(api_include_sharp_client LANGUAGES CSharp)
cmake_minimum_required(VERSION 3.8.2)

file(GLOB_RECURSE SRCS ${api_include_sharp_client_SOURCE_DIR}/../library/Example/sharp_output/*.cs) 

add_executable(api_include_sharp_client
  ${api_include_sharp_client_SOURCE_DIR}/Program.cs
  ${api_include_sharp_client_SOURCE_DIR}/Properties/AssemblyInfo.cs  
  ${api_include_sharp_client_SOURCE_DIR}/Properties/Program.cs
  ${SRCS}
)

target_compile_options(api_include_sharp_client PRIVATE "/unsafe")
SET_TARGET_PROPERTIES(api_include_sharp_client PROPERTIES LINKER_LANGUAGE CSharp)
if(TARGET api_include)
    
  add_dependencies(api_include_sharp_client api_include)
endif()
