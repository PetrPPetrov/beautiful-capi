#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2016 Petr Petrovich Petrov
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


cmake_minimum_required(VERSION 2.8)

function(add_capi_generation generated_source)
    if (NOT generated_source)
        set(generated_source "${CMAKE_CURRENT_SOURCE_DIR}/source/AutoGenWrap.cpp")
    add_custom_command(
        OUTPUT
            ${generated_source}
        COMMAND
            ${PYTHON_EXECUTABLE}
            ${examples_SOURCE_DIR}/../source/Main.py
            -i ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.xml
            -p ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_params.xml
            -o ${CMAKE_CURRENT_SOURCE_DIR}/include
            -w ${generated_source}
        MAIN_DEPENDENCY
            ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.xml
        DEPENDS
            ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_params.xml
        WORKING_DIRECTORY
            ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction(add_capi_generation)

function(add_cs_api_generation cs_api_module_dir module_name)
    add_custom_command(
        TARGET
            ${PROJECT_NAME}
        PRE_BUILD
        COMMAND
            ${PYTHON_EXECUTABLE}
            ARGS
                ${examples_SOURCE_DIR}/../source/CSharp.py
                -i ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.xml
                -p ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_params.xml
                -o ${CMAKE_CURRENT_SOURCE_DIR}/${cs_api_module_dir}
                -m ${module_name}
        WORKING_DIRECTORY
            ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction()
