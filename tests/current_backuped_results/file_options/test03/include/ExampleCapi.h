/*
 * Beautiful Capi generates beautiful C API wrappers for your C++ classes
 * Copyright (C) 2015 Petr Petrovich Petrov
 *
 * This file is part of Beautiful Capi.
 *
 * Beautiful Capi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Beautiful Capi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

/*
 * WARNING: This file was automatically generated by Beautiful Capi!
 * Do not edit this file! Please edit the source API description.
 */

#ifndef EXAMPLE_CAPI_INCLUDED
#define EXAMPLE_CAPI_INCLUDED

#ifdef __cplusplus
    #define EXAMPLE_CAPI_PREFIX extern "C"
#else
    #define EXAMPLE_CAPI_PREFIX
#endif

#ifdef _WIN32
    #ifdef __GNUC__
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX __attribute__ ((dllimport))
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX __declspec(dllimport)
        #define EXAMPLE_API_CONVENTION __cdecl
    #endif
#elif __APPLE__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX
    #endif
    #if defined __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXAMPLE_API_CONVENTION
    #endif
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX
    #endif
    #if defined __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXAMPLE_API_CONVENTION
    #endif
#else
    #error "Unknown platform"
#endif

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_geometry_brep_body_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_geometry_brep_body_new();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_geometry_brep_body_delete(void* object_pointer);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_geometry_brep_body_getname(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_geometry_brep_body_setname(void* object_pointer, const char* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_geometry_sphere_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_geometry_sphere_new();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_geometry_sphere_delete(void* object_pointer);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_geometry_sphere_getradius(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_geometry_sphere_setradius(void* object_pointer, double value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_scene_node_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_scene_node_new();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scene_node_delete(void* object_pointer);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_scene_node_getname(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scene_node_setname(void* object_pointer, const char* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_new();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_delete(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_show(void* object_pointer, const char* text);

#endif /* EXAMPLE_CAPI_INCLUDED */
