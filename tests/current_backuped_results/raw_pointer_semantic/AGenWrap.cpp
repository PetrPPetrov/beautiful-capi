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
#include "PrinterImpl.h"
#include "DumperImpl.h"

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

int AutoGen_Internal_RawPointerSemantic_ExampleGetMajorVersionImpl()
{
    return 1;
}

int AutoGen_Internal_RawPointerSemantic_ExampleGetMinorVersionImpl()
{
    return 0;
}

int AutoGen_Internal_RawPointerSemantic_ExampleGetPatchVersionImpl()
{
    return 0;
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_major_version()
{
    return AutoGen_Internal_RawPointerSemantic_ExampleGetMajorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_minor_version()
{
    return AutoGen_Internal_RawPointerSemantic_ExampleGetMinorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_patch_version()
{
    return AutoGen_Internal_RawPointerSemantic_ExampleGetPatchVersionImpl();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_new()
{
    return new Example::PrinterImpl();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_show(void* object_pointer, const char* text)
{
    Example::PrinterImpl* self = static_cast<Example::PrinterImpl*>(object_pointer);
    self->Show(text);
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_delete(void* object_pointer)
{
    delete static_cast<Example::PrinterImpl*>(object_pointer);
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_new()
{
    return new Example::DumperImpl();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_get_printer(void* object_pointer)
{
    const Example::DumperImpl* self = static_cast<Example::DumperImpl*>(object_pointer);
    return self->GetPrinter();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_set_printer(void* object_pointer, void* printer)
{
    Example::DumperImpl* self = static_cast<Example::DumperImpl*>(object_pointer);
    self->SetPrinter(static_cast<Example::PrinterImpl*>(printer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_dump(void* object_pointer)
{
    const Example::DumperImpl* self = static_cast<Example::DumperImpl*>(object_pointer);
    self->Dump();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_copy(void* object_pointer)
{
    return new Example::DumperImpl(*static_cast<Example::DumperImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_delete(void* object_pointer)
{
    delete static_cast<Example::DumperImpl*>(object_pointer);
}
