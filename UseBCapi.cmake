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

function(add_bcapi_generation)
    set(options clean version verbose)
    set(oneValueArgs workingdir capi input params output snippets wrap sharp tests keys)
    set(multiValueArgs)
    cmake_parse_arguments(arg "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if (arg_workingdir)
        set(working_dir ${arg_workingdir})
    else()
        set(working_dir ${CMAKE_CURRENT_SOURCE_DIR})
    endif()

    if (arg_capi)
        set(capi ${arg_capi})
    else()
        set(capi ${beautiful_capi_SOURCE_DIR}/source/Capi.py)
    endif()

    if (arg_input)
        set(input ${arg_input})
    else()
        set(input ${working_dir}/${PROJECT_NAME}.xml)
    endif()

    if (arg_params)
        set(params ${arg_params})
    else()
        set(params ${working_dir}/${PROJECT_NAME}_params.xml)
    endif()        

    if (arg_output)
        set(output ${arg_output})
    else()
        set(output ${working_dir}/include)
    endif()

    if (${CSHARP_ENABLED} AND arg_sharp)
        set(sharp_output "-S${working_dir}/${arg_sharp}")
    else()
        set(sharp_output "")
    endif()
        
    if (arg_snippets)
        set(snippets ${arg_snippets})
    else()
        set(snippets ${working_dir}/source/snippets)
    endif()

    if (arg_wrap)
        set(wrap ${working_dir}/${arg_wrap})
    else()
        set(wrap ${working_dir}/source/AutoGenWrap.cpp)
    endif()

    if (arg_tests)
        set(tests -t ${working_dir}/${arg_tests})
    else()
        set(tests "")
    endif()
    
    if (arg_keys)
        set(keys -k ${working_dir}/${arg_keys})
    else()
        set(keys "")
    endif()

    if (arg_clean)
        set(clean -c)
    else()
        set(clean "")
    endif()

    if (arg_version)
        set(version -v)
    else()
        set(version "")
    endif()

    if (arg_verbose)
        set(verbose --verbosity)
    else()
        set(verbose "")
    endif()  

    # run at the configuration stage to generate a C# source
    execute_process(
        COMMAND ${PYTHON_EXECUTABLE} ${capi}
            -i ${input}
            -p ${params}
            -o ${output}
            -s ${snippets}
            -w ${wrap}
            ${sharp_output}
            ${tests}
            ${keys}
            ${clean}
            ${version}
            ${verbose}
        WORKING_DIRECTORY
            ${working_dir}
    )

    # run at the Build stage if MAIN_DEPENDENCY or DEPENDS are changed
    add_custom_command(
        OUTPUT
            ${wrap}
        COMMAND
            ${PYTHON_EXECUTABLE}
            ${capi}
            -i ${input}
            -p ${params}
            -o ${output}
            -s ${snippets}
            -w ${wrap}
            ${sharp_output}
            ${tests}
            ${keys}
            ${clean}
            ${version}
            ${verbose}
        MAIN_DEPENDENCY
            ${input}
        DEPENDS
            ${params}
        WORKING_DIRECTORY
            ${working_dir}
    )

endfunction(add_bcapi_generation)
