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

#ifndef BEAUTIFUL_CAPI_EXCEPTION_EXCEPTION_INFO_DEFINED
#define BEAUTIFUL_CAPI_EXCEPTION_EXCEPTION_INFO_DEFINED

struct beautiful_capi_exception_exception_info_t
{
    int code; /* value from beautiful_capi_exception_exception_code_t enumeration */
    void* object_pointer;
};

enum beautiful_capi_exception_exception_code_t
{
    no_exception = 0,
    exception_generic = 1,
    exception_bad_argument = 2,
    exception_null_argument = 3,
    exception_division_by_zero = 4,
    unknown_exception = -1
};

#endif /* BEAUTIFUL_CAPI_EXCEPTION_EXCEPTION_INFO_DEFINED */

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

#ifndef EXAMPLE_CAPI_USE_DYNAMIC_LOADER

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_new(beautiful_capi_exception_exception_info_t* exception_info);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_printer_show(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer, const char* text);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_power_on(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_power_off(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_copy(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_delete(void* object_pointer);
EXAMPLE_API void* EXAMPLE_API_CONVENTION example_scanner_new(beautiful_capi_exception_exception_info_t* exception_info);
EXAMPLE_API const char* EXAMPLE_API_CONVENTION example_scanner_scan_text(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scanner_power_on(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scanner_power_off(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scanner_add_ref(void* object_pointer);
EXAMPLE_API void EXAMPLE_API_CONVENTION example_scanner_release(void* object_pointer);

#else /* EXAMPLE_CAPI_USE_DYNAMIC_LOADER */

typedef void* (EXAMPLE_API_CONVENTION *example_printer_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef const char* (EXAMPLE_API_CONVENTION *example_printer_show_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer, const char* text);
typedef void (EXAMPLE_API_CONVENTION *example_printer_power_on_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_printer_power_off_function_type)(void* object_pointer);
typedef void* (EXAMPLE_API_CONVENTION *example_printer_copy_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_printer_delete_function_type)(void* object_pointer);
typedef void* (EXAMPLE_API_CONVENTION *example_scanner_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef const char* (EXAMPLE_API_CONVENTION *example_scanner_scan_text_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_scanner_power_on_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_scanner_power_off_function_type)(void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_scanner_add_ref_function_type)(void* object_pointer);
typedef void (EXAMPLE_API_CONVENTION *example_scanner_release_function_type)(void* object_pointer);

#ifdef EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS

extern example_printer_new_function_type example_printer_new = 0;
extern example_printer_show_function_type example_printer_show = 0;
extern example_printer_power_on_function_type example_printer_power_on = 0;
extern example_printer_power_off_function_type example_printer_power_off = 0;
extern example_printer_copy_function_type example_printer_copy = 0;
extern example_printer_delete_function_type example_printer_delete = 0;
extern example_scanner_new_function_type example_scanner_new = 0;
extern example_scanner_scan_text_function_type example_scanner_scan_text = 0;
extern example_scanner_power_on_function_type example_scanner_power_on = 0;
extern example_scanner_power_off_function_type example_scanner_power_off = 0;
extern example_scanner_add_ref_function_type example_scanner_add_ref = 0;
extern example_scanner_release_function_type example_scanner_release = 0;

#else /* EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS */

extern example_printer_new_function_type example_printer_new;
extern example_printer_show_function_type example_printer_show;
extern example_printer_power_on_function_type example_printer_power_on;
extern example_printer_power_off_function_type example_printer_power_off;
extern example_printer_copy_function_type example_printer_copy;
extern example_printer_delete_function_type example_printer_delete;
extern example_scanner_new_function_type example_scanner_new;
extern example_scanner_scan_text_function_type example_scanner_scan_text;
extern example_scanner_power_on_function_type example_scanner_power_on;
extern example_scanner_power_off_function_type example_scanner_power_off;
extern example_scanner_add_ref_function_type example_scanner_add_ref;
extern example_scanner_release_function_type example_scanner_release;

#endif /* EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS */

#ifdef __cplusplus

#include <stdexcept>
#include <sstream>
#ifdef _WIN32
#include <Windows.h>
#else
#include <dlfcn.h>
#endif

namespace Example
{
    class Initialization
    {
        #ifdef _WIN32
        HINSTANCE handle;
        #else
        void* handle;
        #endif
        
        template<class FunctionPointerType>
        void load_function(FunctionPointerType& to_init, const char* name)
        {
            #ifdef _WIN32
            to_init = reinterpret_cast<FunctionPointerType>(GetProcAddress(handle, name));
            #else
            to_init = reinterpret_cast<FunctionPointerType>(dlsym(handle, name));
            #endif
            if (!to_init)
            {
                std::stringstream error_message;
                error_message << "Can't obtain function " << name;
                throw std::runtime_error(error_message.str());
            }
        }
        
        Initialization();
        Initialization(const Initialization&);
    public:
        Initialization(const char* name)
        {
            if (!name) throw std::runtime_error("Null library name was passed");
            #ifdef _WIN32
            handle = LoadLibraryA(name);
            #else
            handle = dlopen(name, RTLD_NOW);
            #endif
            if (!handle)
            {
                std::stringstream error_message;
                error_message << "Can't load shared library " << name;
                throw std::runtime_error(error_message.str());
            }
            
            load_function<example_printer_new_function_type>(example_printer_new, "example_printer_new");
            load_function<example_printer_show_function_type>(example_printer_show, "example_printer_show");
            load_function<example_printer_power_on_function_type>(example_printer_power_on, "example_printer_power_on");
            load_function<example_printer_power_off_function_type>(example_printer_power_off, "example_printer_power_off");
            load_function<example_printer_copy_function_type>(example_printer_copy, "example_printer_copy");
            load_function<example_printer_delete_function_type>(example_printer_delete, "example_printer_delete");
            load_function<example_scanner_new_function_type>(example_scanner_new, "example_scanner_new");
            load_function<example_scanner_scan_text_function_type>(example_scanner_scan_text, "example_scanner_scan_text");
            load_function<example_scanner_power_on_function_type>(example_scanner_power_on, "example_scanner_power_on");
            load_function<example_scanner_power_off_function_type>(example_scanner_power_off, "example_scanner_power_off");
            load_function<example_scanner_add_ref_function_type>(example_scanner_add_ref, "example_scanner_add_ref");
            load_function<example_scanner_release_function_type>(example_scanner_release, "example_scanner_release");
        }
        ~Initialization()
        {
            #ifdef _WIN32
            FreeLibrary(handle);
            #else
            dlclose(handle);
            #endif
        }
    };
}

#endif /* __cplusplus */

#endif /* EXAMPLE_CAPI_USE_DYNAMIC_LOADER */

#endif /* EXAMPLE_CAPI_INCLUDED */

