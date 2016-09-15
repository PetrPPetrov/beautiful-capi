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

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_cast_to_example_vectorofobjectsderived_examplemodelptr_float(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_cast_to_example_vectorofobjectsderived_examplemodelptr_double(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position_float_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_float_delete(void* object_pointer);
EXAMPLE_API float EXAMPLE_API_CONVENTION example_position_float_getx(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_float_setx(void* object_pointer, float x);
EXAMPLE_API float EXAMPLE_API_CONVENTION example_position_float_gety(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_float_sety(void* object_pointer, float y);
EXAMPLE_API float EXAMPLE_API_CONVENTION example_position_float_getz(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_float_setz(void* object_pointer, float z);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position_double_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_double_delete(void* object_pointer);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_position_double_getx(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_double_setx(void* object_pointer, double x);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_position_double_gety(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_double_sety(void* object_pointer, double y);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_position_double_getz(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position_double_setz(void* object_pointer, double z);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_float_cast_to_base(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_float_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position4d_float_delete(void* object_pointer);
EXAMPLE_API float EXAMPLE_API_CONVENTION example_position4d_float_getw(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position4d_float_setw(void* object_pointer, float x);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_double_cast_to_base(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_double_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_position4d_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position4d_double_delete(void* object_pointer);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_position4d_double_getw(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_position4d_double_setw(void* object_pointer, double x);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_float_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_model_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_float_release(void* object_pointer);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_model_float_getname(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_float_setname(void* object_pointer, const char* name);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_model_float_getposition(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_float_setposition(void* object_pointer, void* position);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_double_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_model_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_double_release(void* object_pointer);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_model_double_getname(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_double_setname(void* object_pointer, const char* name);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_model_double_getposition(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_model_double_setposition(void* object_pointer, void* position);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_int_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_int_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_int_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_int_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_int_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_int_pushback(void* object_pointer, int value);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_int_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_double_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_double_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_double_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_double_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_double_pushback(void* object_pointer, double value);
EXAMPLE_API double EXAMPLE_API_CONVENTION example_vectorof_double_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_float_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition_double_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_float_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_exampleposition4d_double_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_copy(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_delete(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorof_examplevectorof_exampleposition4d_float_getitem(void* object_pointer, int index);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_release(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_float_getitem(void* object_pointer, int index);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_release(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_getsize(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_clear(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_pushback(void* object_pointer, void* value);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjects_examplemodelptr_double_getitem(void* object_pointer, int index);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_float_cast_to_base(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_float_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_float_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_float_release(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_float_geta(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_double_cast_to_base(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_double_add_ref(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_double_default();
EXAMPLE_API void EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_double_release(void* object_pointer);
EXAMPLE_API int EXAMPLE_API_CONVENTION example_vectorofobjectsderived_examplemodelptr_double_geta(void* object_pointer);

#endif /* EXAMPLE_CAPI_INCLUDED */

