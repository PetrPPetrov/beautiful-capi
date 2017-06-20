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

#include <stdexcept>
#include <cassert>
#include "ClassA.h"
#include "ClassB.h"
#include "ClassC.h"

#ifdef _WIN32
    #ifdef __GNUC__
        #define CLASSES_API extern "C" __attribute__ ((dllexport))
        #define CLASSES_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define CLASSES_API extern "C" __declspec(dllexport)
        #define CLASSES_API_CONVENTION __cdecl
    #endif
#elif __APPLE__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define CLASSES_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define CLASSES_API extern "C"
    #endif
    #ifdef __i386__
        #define CLASSES_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define CLASSES_API_CONVENTION
    #endif /* __i386__ */
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define CLASSES_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define CLASSES_API extern "C"
    #endif
    #ifdef __i386__
        #define CLASSES_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define CLASSES_API_CONVENTION
    #endif /* __i386__ */
#else
    #error "Unknown platform"
#endif

int AutoGen_Internal_Classes_ClassesGetMajorVersionImpl()
{
    return 1;
}

int AutoGen_Internal_Classes_ClassesGetMinorVersionImpl()
{
    return 0;
}

int AutoGen_Internal_Classes_ClassesGetPatchVersionImpl()
{
    return 0;
}

CLASSES_API int CLASSES_API_CONVENTION classes_get_major_version()
{
    return AutoGen_Internal_Classes_ClassesGetMajorVersionImpl();
}

CLASSES_API int CLASSES_API_CONVENTION classes_get_minor_version()
{
    return AutoGen_Internal_Classes_ClassesGetMinorVersionImpl();
}

CLASSES_API int CLASSES_API_CONVENTION classes_get_patch_version()
{
    return AutoGen_Internal_Classes_ClassesGetPatchVersionImpl();
}

CLASSES_API void* CLASSES_API_CONVENTION classes_class_a_default()
{
    return new Classes::ClassA();
}

CLASSES_API int CLASSES_API_CONVENTION classes_class_a_get_value_const(void* object_pointer)
{
    const Classes::ClassA* self = static_cast<Classes::ClassA*>(object_pointer);
    return self->GetValue();
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_a_set_value(void* object_pointer, int value)
{
    Classes::ClassA* self = static_cast<Classes::ClassA*>(object_pointer);
    self->SetValue(value);
}

CLASSES_API void* CLASSES_API_CONVENTION classes_class_a_copy(void* object_pointer)
{
    return new Classes::ClassA(*static_cast<Classes::ClassA*>(object_pointer));
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_a_delete(void* object_pointer)
{
    delete static_cast<Classes::ClassA*>(object_pointer);
}

CLASSES_API void* CLASSES_API_CONVENTION classes_class_b_default()
{
    return new Classes::ClassB();
}

CLASSES_API const char* CLASSES_API_CONVENTION classes_class_b_get_value_const(void* object_pointer)
{
    const Classes::ClassB* self = static_cast<Classes::ClassB*>(object_pointer);
    return self->GetValue();
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_b_set_value(void* object_pointer, const char* value)
{
    Classes::ClassB* self = static_cast<Classes::ClassB*>(object_pointer);
    self->SetValue(value);
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_b_delete(void* object_pointer)
{
    delete static_cast<Classes::ClassB*>(object_pointer);
}

CLASSES_API void* CLASSES_API_CONVENTION classes_class_c_default()
{
    return new Classes::ClassC();
}

CLASSES_API double CLASSES_API_CONVENTION classes_class_c_get_value_const(void* object_pointer)
{
    const Classes::ClassC* self = static_cast<Classes::ClassC*>(object_pointer);
    return self->GetValue();
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_c_set_value(void* object_pointer, double value)
{
    Classes::ClassC* self = static_cast<Classes::ClassC*>(object_pointer);
    self->SetValue(value);
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_c_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Classes::ClassC*>(object_pointer));
}

CLASSES_API void CLASSES_API_CONVENTION classes_class_c_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Classes::ClassC*>(object_pointer));
}