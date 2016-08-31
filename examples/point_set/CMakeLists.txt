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

project(point_set_example)

cmake_minimum_required(VERSION 2.8)

find_path(boost_core_found enable_if.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/core/include/boost/core/ NO_DEFAULT_PATH)
find_path(boost_config_found config.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/config/include/boost/ NO_DEFAULT_PATH)
find_path(boost_assert_found assert.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/assert/include/boost/ NO_DEFAULT_PATH)
find_path(boost_throw_exception_found throw_exception.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/throw_exception/include/boost/ NO_DEFAULT_PATH)
find_path(boost_predef_found predef.h ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/predef/include/boost/ NO_DEFAULT_PATH)
find_path(boost_smart_ptr_found smart_ptr.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/smart_ptr/include/boost/ NO_DEFAULT_PATH)
find_path(boost_type_traits_found type_traits.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/type_traits/include/boost/ NO_DEFAULT_PATH)
find_path(boost_static_assert_found static_assert.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/static_assert/include/boost/ NO_DEFAULT_PATH)
find_path(boost_align_found align.hpp ${point_set_example_SOURCE_DIR}/../../3rdparty/boost/align/include/boost/ NO_DEFAULT_PATH)

if(boost_core_found AND boost_config_found AND boost_assert_found AND boost_throw_exception_found AND
   boost_predef_found AND boost_smart_ptr_found AND boost_type_traits_found AND boost_static_assert_found AND
   boost_align_found)
  add_subdirectory(library)
  add_subdirectory(client)
else()
  message(STATUS "Boost components are not found. Please update boost submodule by git submodule init, git submodule update commands.")
endif()

