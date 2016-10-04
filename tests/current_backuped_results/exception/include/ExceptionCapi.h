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

#ifndef EXCEPTION_CAPI_INCLUDED
#define EXCEPTION_CAPI_INCLUDED

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
    #define EXCEPTION_CAPI_PREFIX extern "C"
#else
    #define EXCEPTION_CAPI_PREFIX
#endif

#ifdef _WIN32
    #ifdef __GNUC__
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX __attribute__ ((dllimport))
        #define EXCEPTION_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX __declspec(dllimport)
        #define EXCEPTION_API_CONVENTION __cdecl
    #endif
#elif __APPLE__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX __attribute__ ((visibility ("default")))
    #else
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX
    #endif
    #if defined __i386__
        #define EXCEPTION_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXCEPTION_API_CONVENTION
    #endif
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX __attribute__ ((visibility ("default")))
    #else
        #define EXCEPTION_API EXCEPTION_CAPI_PREFIX
    #endif
    #if defined __i386__
        #define EXCEPTION_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXCEPTION_API_CONVENTION
    #endif
#else
    #error "Unknown platform"
#endif

#ifndef EXCEPTION_CAPI_USE_DYNAMIC_LOADER

EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_generic_new(beautiful_capi_exception_exception_info_t* exception_info);
EXCEPTION_API const char* EXCEPTION_API_CONVENTION exception_generic_get_error_text(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_generic_copy(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXCEPTION_API void EXCEPTION_API_CONVENTION exception_generic_delete(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_bad_argument_new(beautiful_capi_exception_exception_info_t* exception_info);
EXCEPTION_API const char* EXCEPTION_API_CONVENTION exception_bad_argument_get_argument_name(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_bad_argument_copy(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXCEPTION_API void EXCEPTION_API_CONVENTION exception_bad_argument_delete(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_bad_argument_cast_to_base(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_null_argument_new(beautiful_capi_exception_exception_info_t* exception_info);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_null_argument_copy(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXCEPTION_API void EXCEPTION_API_CONVENTION exception_null_argument_delete(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_null_argument_cast_to_base(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_division_by_zero_new(beautiful_capi_exception_exception_info_t* exception_info);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_division_by_zero_copy(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
EXCEPTION_API void EXCEPTION_API_CONVENTION exception_division_by_zero_delete(void* object_pointer);
EXCEPTION_API void* EXCEPTION_API_CONVENTION exception_division_by_zero_cast_to_base(void* object_pointer);

#else /* EXCEPTION_CAPI_USE_DYNAMIC_LOADER */

typedef void* (EXCEPTION_API_CONVENTION *exception_generic_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef const char* (EXCEPTION_API_CONVENTION *exception_generic_get_error_text_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_generic_copy_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXCEPTION_API_CONVENTION *exception_generic_delete_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_bad_argument_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef const char* (EXCEPTION_API_CONVENTION *exception_bad_argument_get_argument_name_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_bad_argument_copy_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXCEPTION_API_CONVENTION *exception_bad_argument_delete_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_bad_argument_cast_to_base_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_null_argument_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef void* (EXCEPTION_API_CONVENTION *exception_null_argument_copy_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXCEPTION_API_CONVENTION *exception_null_argument_delete_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_null_argument_cast_to_base_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_division_by_zero_new_function_type)(beautiful_capi_exception_exception_info_t* exception_info);
typedef void* (EXCEPTION_API_CONVENTION *exception_division_by_zero_copy_function_type)(beautiful_capi_exception_exception_info_t* exception_info, void* object_pointer);
typedef void (EXCEPTION_API_CONVENTION *exception_division_by_zero_delete_function_type)(void* object_pointer);
typedef void* (EXCEPTION_API_CONVENTION *exception_division_by_zero_cast_to_base_function_type)(void* object_pointer);

#ifdef EXCEPTION_CAPI_DEFINE_FUNCTION_POINTERS

extern exception_generic_new_function_type exception_generic_new = 0;
extern exception_generic_get_error_text_function_type exception_generic_get_error_text = 0;
extern exception_generic_copy_function_type exception_generic_copy = 0;
extern exception_generic_delete_function_type exception_generic_delete = 0;
extern exception_bad_argument_new_function_type exception_bad_argument_new = 0;
extern exception_bad_argument_get_argument_name_function_type exception_bad_argument_get_argument_name = 0;
extern exception_bad_argument_copy_function_type exception_bad_argument_copy = 0;
extern exception_bad_argument_delete_function_type exception_bad_argument_delete = 0;
extern exception_bad_argument_cast_to_base_function_type exception_bad_argument_cast_to_base = 0;
extern exception_null_argument_new_function_type exception_null_argument_new = 0;
extern exception_null_argument_copy_function_type exception_null_argument_copy = 0;
extern exception_null_argument_delete_function_type exception_null_argument_delete = 0;
extern exception_null_argument_cast_to_base_function_type exception_null_argument_cast_to_base = 0;
extern exception_division_by_zero_new_function_type exception_division_by_zero_new = 0;
extern exception_division_by_zero_copy_function_type exception_division_by_zero_copy = 0;
extern exception_division_by_zero_delete_function_type exception_division_by_zero_delete = 0;
extern exception_division_by_zero_cast_to_base_function_type exception_division_by_zero_cast_to_base = 0;

#else /* EXCEPTION_CAPI_DEFINE_FUNCTION_POINTERS */

extern exception_generic_new_function_type exception_generic_new;
extern exception_generic_get_error_text_function_type exception_generic_get_error_text;
extern exception_generic_copy_function_type exception_generic_copy;
extern exception_generic_delete_function_type exception_generic_delete;
extern exception_bad_argument_new_function_type exception_bad_argument_new;
extern exception_bad_argument_get_argument_name_function_type exception_bad_argument_get_argument_name;
extern exception_bad_argument_copy_function_type exception_bad_argument_copy;
extern exception_bad_argument_delete_function_type exception_bad_argument_delete;
extern exception_bad_argument_cast_to_base_function_type exception_bad_argument_cast_to_base;
extern exception_null_argument_new_function_type exception_null_argument_new;
extern exception_null_argument_copy_function_type exception_null_argument_copy;
extern exception_null_argument_delete_function_type exception_null_argument_delete;
extern exception_null_argument_cast_to_base_function_type exception_null_argument_cast_to_base;
extern exception_division_by_zero_new_function_type exception_division_by_zero_new;
extern exception_division_by_zero_copy_function_type exception_division_by_zero_copy;
extern exception_division_by_zero_delete_function_type exception_division_by_zero_delete;
extern exception_division_by_zero_cast_to_base_function_type exception_division_by_zero_cast_to_base;

#endif /* EXCEPTION_CAPI_DEFINE_FUNCTION_POINTERS */

#ifdef __cplusplus

#include <stdexcept>
#include <sstream>
#ifdef _WIN32
#include <Windows.h>
#else
#include <dlfcn.h>
#endif

namespace Exception
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
            
            load_function<exception_generic_new_function_type>(exception_generic_new, "exception_generic_new");
            load_function<exception_generic_get_error_text_function_type>(exception_generic_get_error_text, "exception_generic_get_error_text");
            load_function<exception_generic_copy_function_type>(exception_generic_copy, "exception_generic_copy");
            load_function<exception_generic_delete_function_type>(exception_generic_delete, "exception_generic_delete");
            load_function<exception_bad_argument_new_function_type>(exception_bad_argument_new, "exception_bad_argument_new");
            load_function<exception_bad_argument_get_argument_name_function_type>(exception_bad_argument_get_argument_name, "exception_bad_argument_get_argument_name");
            load_function<exception_bad_argument_copy_function_type>(exception_bad_argument_copy, "exception_bad_argument_copy");
            load_function<exception_bad_argument_delete_function_type>(exception_bad_argument_delete, "exception_bad_argument_delete");
            load_function<exception_bad_argument_cast_to_base_function_type>(exception_bad_argument_cast_to_base, "exception_bad_argument_cast_to_base");
            load_function<exception_null_argument_new_function_type>(exception_null_argument_new, "exception_null_argument_new");
            load_function<exception_null_argument_copy_function_type>(exception_null_argument_copy, "exception_null_argument_copy");
            load_function<exception_null_argument_delete_function_type>(exception_null_argument_delete, "exception_null_argument_delete");
            load_function<exception_null_argument_cast_to_base_function_type>(exception_null_argument_cast_to_base, "exception_null_argument_cast_to_base");
            load_function<exception_division_by_zero_new_function_type>(exception_division_by_zero_new, "exception_division_by_zero_new");
            load_function<exception_division_by_zero_copy_function_type>(exception_division_by_zero_copy, "exception_division_by_zero_copy");
            load_function<exception_division_by_zero_delete_function_type>(exception_division_by_zero_delete, "exception_division_by_zero_delete");
            load_function<exception_division_by_zero_cast_to_base_function_type>(exception_division_by_zero_cast_to_base, "exception_division_by_zero_cast_to_base");
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

#endif /* EXCEPTION_CAPI_USE_DYNAMIC_LOADER */

#endif /* EXCEPTION_CAPI_INCLUDED */

