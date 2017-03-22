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
#include "PageImpl.h"
#include "DocumentImpl.h"

#ifdef _WIN32
    #ifdef __GNUC__
        #define EXAMPLE_API extern "C" __attribute__ ((dllexport))
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXAMPLE_API extern "C" __declspec(dllexport)
        #define EXAMPLE_API_CONVENTION __cdecl
    #endif
#elif __APPLE__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API extern "C"
    #endif
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API extern "C"
    #endif
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#else
    #error "Unknown platform"
#endif

int AutoGen_Internal_ObjectParameter_ExampleGetMajorVersionImpl()
{
    return 1;
}

int AutoGen_Internal_ObjectParameter_ExampleGetMinorVersionImpl()
{
    return 0;
}

int AutoGen_Internal_ObjectParameter_ExampleGetPatchVersionImpl()
{
    return 0;
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_major_version()
{
    return AutoGen_Internal_ObjectParameter_ExampleGetMajorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_minor_version()
{
    return AutoGen_Internal_ObjectParameter_ExampleGetMinorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_patch_version()
{
    return AutoGen_Internal_ObjectParameter_ExampleGetPatchVersionImpl();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_page_default()
{
    return new Example::PageImpl();
}

EXAMPLE_API size_t EXAMPLE_API_CONVENTION example_page_get_width_const(void* object_pointer)
{
    const Example::PageImpl* self = static_cast<Example::PageImpl*>(object_pointer);
    return self->GetWidth();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_page_set_width(void* object_pointer, size_t width)
{
    Example::PageImpl* self = static_cast<Example::PageImpl*>(object_pointer);
    self->SetWidth(width);
}

EXAMPLE_API size_t EXAMPLE_API_CONVENTION example_page_get_height_const(void* object_pointer)
{
    const Example::PageImpl* self = static_cast<Example::PageImpl*>(object_pointer);
    return self->GetHeight();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_page_set_height(void* object_pointer, size_t height)
{
    Example::PageImpl* self = static_cast<Example::PageImpl*>(object_pointer);
    self->SetHeight(height);
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_page_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::PageImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_page_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::PageImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_document_default()
{
    return new Example::DocumentImpl();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_document_show_const(void* object_pointer)
{
    const Example::DocumentImpl* self = static_cast<Example::DocumentImpl*>(object_pointer);
    self->Show();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_document_get_page_const(void* object_pointer)
{
    const Example::DocumentImpl* self = static_cast<Example::DocumentImpl*>(object_pointer);
    return self->GetPage();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_document_set_page(void* object_pointer, void* value)
{
    Example::DocumentImpl* self = static_cast<Example::DocumentImpl*>(object_pointer);
    self->SetPage(static_cast<Example::PageImpl*>(value));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_document_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::DocumentImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_document_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::DocumentImpl*>(object_pointer));
}
