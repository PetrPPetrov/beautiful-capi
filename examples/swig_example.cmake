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


function(add_swig_generation swig_module_dir module_name)
    if(SWIG_FOUND AND EXISTS ${SWIG_USE_FILE})
        add_custom_command(
            OUTPUT
                ${CMAKE_CURRENT_SOURCE_DIR}/${swig_module_dir}/${module_name}.i
            COMMAND
                ${PYTHON_EXECUTABLE}
                ${examples_SOURCE_DIR}/../source/Swig.py
                -i ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.xml
                -p ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_params.xml
                -o ${CMAKE_CURRENT_SOURCE_DIR}/${swig_module_dir}
                -m ${module_name}
            MAIN_DEPENDENCY
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.xml
            DEPENDS
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_params.xml
            WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    endif()
endfunction()


find_package(SWIG)


macro(setup_swig_module swig_module_dir module_name)
    if(SWIG_FOUND AND EXISTS ${SWIG_USE_FILE})
        include("${SWIG_USE_FILE}")
        include_directories("${CMAKE_CURRENT_SOURCE_DIR}/source")

        if(NOT EXISTS ${swig_module_dir}/${module_name}.i)
            file(WRITE ${swig_module_dir}/${module_name}.i "Temporary_file_to_generate_project")
        endif()

        set_property(SOURCE ${swig_module_dir}/${module_name}.i PROPERTY SWIG_MODULE_NAME ${module_name})
        set_property(SOURCE ${swig_module_dir}/${module_name}.i PROPERTY CPLUSPLUS ON)
        set_source_files_properties( ${swig_generated_file_fullname} PROPERTIES COMPILE_FLAGS "-bigobj")
    endif()
endmacro()


macro(add_swig_python swig_module_dir module_name)
    if(SWIG_FOUND AND EXISTS ${SWIG_USE_FILE})
        find_package(PythonLibs)
        include_directories(${PYTHON_INCLUDE_PATH})

        set(CMAKE_SWIG_OUTDIR "${CMAKE_CURRENT_SOURCE_DIR}/${swig_module_dir}_python")
        swig_add_module(${PROJECT_NAME}_python python ${swig_module_dir}/${module_name}.i)
        swig_link_libraries(${PROJECT_NAME}_python ${PROJECT_NAME} ${PYTHON_LIBRARIES})
    endif()
endmacro()


macro(add_swig_csharp swig_module_dir module_name)
    if(SWIG_FOUND AND EXISTS ${SWIG_USE_FILE})
        set(CMAKE_SWIG_OUTDIR "${CMAKE_CURRENT_SOURCE_DIR}/${swig_module_dir}_csharp")
        swig_add_module(${PROJECT_NAME}_csharp csharp ${swig_module_dir}/${module_name}.i)
        swig_link_libraries(${PROJECT_NAME}_csharp ${PROJECT_NAME})
    endif()
endmacro()
