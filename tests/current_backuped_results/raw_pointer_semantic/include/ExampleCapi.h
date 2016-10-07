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
#else /* __cplusplus */
    #define EXAMPLE_CAPI_PREFIX
#endif /* __cplusplus */

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
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API EXAMPLE_CAPI_PREFIX
    #endif
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#else
    #error "Unknown platform"
#endif

#define EXAMPLE_MAJOR_VERSION 1
#define EXAMPLE_MINOR_VERSION 0
#define EXAMPLE_PATCH_VERSION 0

#ifdef __cplusplus
    #ifdef _MSC_VER
        #if _MSC_VER >= 1900
            #define EXAMPLE_NOEXCEPT noexcept
        #else /* _MSC_VER >= 1900 */
            #define EXAMPLE_NOEXCEPT
        #endif /* _MSC_VER >= 1900 */
        #if _MSC_VER >= 1600
            #define EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
        #endif /* _MSC_VER >= 1600 */
        #if _MSC_VER >= 1800
            #define EXAMPLE_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE
        #endif /* _MSC_VER >= 1800 */
    #else /* _MSC_VER */
        #if __cplusplus >= 201103L
            #define EXAMPLE_NOEXCEPT noexcept
            #define EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
            #define EXAMPLE_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE
        #else /* __cplusplus >= 201103L */
            #define EXAMPLE_NOEXCEPT
        #endif /* __cplusplus >= 201103L */
    #endif /* _MSC_VER */
#endif /* __cplusplus */

#ifndef EXAMPLE_CAPI_USE_DYNAMIC_LOADER
    
    EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_major_version();
    EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_minor_version();
    EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_patch_version();
    EXAMPLE_API void* EXAMPLE_API_CONVENTION example_printer_new();
    EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_show(void* object_pointer, const char* text);
    EXAMPLE_API void EXAMPLE_API_CONVENTION example_printer_delete(void* object_pointer);
    EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_new();
    EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_get_printer(void* object_pointer);
    EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_set_printer(void* object_pointer, void* printer);
    EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_dump(void* object_pointer);
    EXAMPLE_API void* EXAMPLE_API_CONVENTION example_dumper_copy(void* object_pointer);
    EXAMPLE_API void EXAMPLE_API_CONVENTION example_dumper_delete(void* object_pointer);
    
    #ifdef __cplusplus
    
    #include <stdexcept>
    #include <sstream>
    
    namespace Example
    {
        class Initialization
        {
        public:
            Initialization()
            {
                const int major_version = example_get_major_version();
                const int minor_version = example_get_minor_version();
                const int patch_version = example_get_patch_version();
                if (major_version != EXAMPLE_MAJOR_VERSION || minor_version != EXAMPLE_MINOR_VERSION || patch_version != EXAMPLE_PATCH_VERSION)
                {
                    std::stringstream error_message;
                    error_message << "Incorrect version of library. ";
                    error_message << "Expected version is " << EXAMPLE_MAJOR_VERSION << "." << EXAMPLE_MINOR_VERSION << "." << EXAMPLE_PATCH_VERSION << ". ";
                    error_message << "Found version is " << major_version << "." << minor_version << "." << patch_version << ".";
                    throw std::runtime_error(error_message.str());
                }
            }
        };
    }
    
    #endif /* __cplusplus */
    
#else /* EXAMPLE_CAPI_USE_DYNAMIC_LOADER */
    
    typedef int (EXAMPLE_API_CONVENTION *example_get_major_version_function_type)();
    typedef int (EXAMPLE_API_CONVENTION *example_get_minor_version_function_type)();
    typedef int (EXAMPLE_API_CONVENTION *example_get_patch_version_function_type)();
    typedef void* (EXAMPLE_API_CONVENTION *example_printer_new_function_type)();
    typedef void (EXAMPLE_API_CONVENTION *example_printer_show_function_type)(void* object_pointer, const char* text);
    typedef void (EXAMPLE_API_CONVENTION *example_printer_delete_function_type)(void* object_pointer);
    typedef void* (EXAMPLE_API_CONVENTION *example_dumper_new_function_type)();
    typedef void* (EXAMPLE_API_CONVENTION *example_dumper_get_printer_function_type)(void* object_pointer);
    typedef void (EXAMPLE_API_CONVENTION *example_dumper_set_printer_function_type)(void* object_pointer, void* printer);
    typedef void (EXAMPLE_API_CONVENTION *example_dumper_dump_function_type)(void* object_pointer);
    typedef void* (EXAMPLE_API_CONVENTION *example_dumper_copy_function_type)(void* object_pointer);
    typedef void (EXAMPLE_API_CONVENTION *example_dumper_delete_function_type)(void* object_pointer);
    
    #ifdef EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS
        
        extern example_get_major_version_function_type example_get_major_version = 0;
        extern example_get_minor_version_function_type example_get_minor_version = 0;
        extern example_get_patch_version_function_type example_get_patch_version = 0;
        extern example_printer_new_function_type example_printer_new = 0;
        extern example_printer_show_function_type example_printer_show = 0;
        extern example_printer_delete_function_type example_printer_delete = 0;
        extern example_dumper_new_function_type example_dumper_new = 0;
        extern example_dumper_get_printer_function_type example_dumper_get_printer = 0;
        extern example_dumper_set_printer_function_type example_dumper_set_printer = 0;
        extern example_dumper_dump_function_type example_dumper_dump = 0;
        extern example_dumper_copy_function_type example_dumper_copy = 0;
        extern example_dumper_delete_function_type example_dumper_delete = 0;
        
    #else /* EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS */
        
        extern example_get_major_version_function_type example_get_major_version;
        extern example_get_minor_version_function_type example_get_minor_version;
        extern example_get_patch_version_function_type example_get_patch_version;
        extern example_printer_new_function_type example_printer_new;
        extern example_printer_show_function_type example_printer_show;
        extern example_printer_delete_function_type example_printer_delete;
        extern example_dumper_new_function_type example_dumper_new;
        extern example_dumper_get_printer_function_type example_dumper_get_printer;
        extern example_dumper_set_printer_function_type example_dumper_set_printer;
        extern example_dumper_dump_function_type example_dumper_dump;
        extern example_dumper_copy_function_type example_dumper_copy;
        extern example_dumper_delete_function_type example_dumper_delete;
        
    #endif /* EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS */
    
    #ifdef __cplusplus
    
    #include <stdexcept>
    #include <sstream>
    
    #ifdef _WIN32
        #include <Windows.h>
    #else /* _WIN32 */
        #include <dlfcn.h>
    #endif /* _WIN32 */
    
    namespace Example
    {
        class Initialization
        {
            #ifdef _WIN32
                HINSTANCE handle;
            #else /* _WIN32 */
                void* handle;
            #endif /* _WIN32 */
            
            template<class FunctionPointerType>
            void load_function(FunctionPointerType& to_init, const char* name)
            {
                #ifdef _WIN32
                    to_init = reinterpret_cast<FunctionPointerType>(GetProcAddress(handle, name));
                #else /* _WIN32 */
                    to_init = reinterpret_cast<FunctionPointerType>(dlsym(handle, name));
                #endif /* _WIN32 */
                if (!to_init)
                {
                    std::stringstream error_message;
                    error_message << "Can't obtain function " << name;
                    throw std::runtime_error(error_message.str());
                }
            }
            
            void load_module(const char* shared_library_name)
            {
                if (!shared_library_name) throw std::runtime_error("Null library name was passed");
                #ifdef _WIN32
                    handle = LoadLibraryA(shared_library_name);
                #else /* _WIN32 */
                    handle = dlopen(shared_library_name, RTLD_NOW);
                #endif /* _WIN32 */
                if (!handle)
                {
                    std::stringstream error_message;
                    error_message << "Can't load shared library " << shared_library_name;
                    throw std::runtime_error(error_message.str());
                }
                load_function<example_get_major_version_function_type>(example_get_major_version, "example_get_major_version");
                load_function<example_get_minor_version_function_type>(example_get_minor_version, "example_get_minor_version");
                load_function<example_get_patch_version_function_type>(example_get_patch_version, "example_get_patch_version");
                load_function<example_printer_new_function_type>(example_printer_new, "example_printer_new");
                load_function<example_printer_show_function_type>(example_printer_show, "example_printer_show");
                load_function<example_printer_delete_function_type>(example_printer_delete, "example_printer_delete");
                load_function<example_dumper_new_function_type>(example_dumper_new, "example_dumper_new");
                load_function<example_dumper_get_printer_function_type>(example_dumper_get_printer, "example_dumper_get_printer");
                load_function<example_dumper_set_printer_function_type>(example_dumper_set_printer, "example_dumper_set_printer");
                load_function<example_dumper_dump_function_type>(example_dumper_dump, "example_dumper_dump");
                load_function<example_dumper_copy_function_type>(example_dumper_copy, "example_dumper_copy");
                load_function<example_dumper_delete_function_type>(example_dumper_delete, "example_dumper_delete");
                const int major_version = example_get_major_version();
                const int minor_version = example_get_minor_version();
                const int patch_version = example_get_patch_version();
                if (major_version != EXAMPLE_MAJOR_VERSION || minor_version != EXAMPLE_MINOR_VERSION || patch_version != EXAMPLE_PATCH_VERSION)
                {
                    std::stringstream error_message;
                    error_message << "Incorrect version of " << shared_library_name << " library. ";
                    error_message << "Expected version is " << EXAMPLE_MAJOR_VERSION << "." << EXAMPLE_MINOR_VERSION << "." << EXAMPLE_PATCH_VERSION << ". ";
                    error_message << "Found version is " << major_version << "." << minor_version << "." << patch_version << ".";
                    throw std::runtime_error(error_message.str());
                }
            }
            
            Initialization();
            Initialization(const Initialization&);
            #ifdef EXAMPLE_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE
                Initialization(Initialization &&) = delete;
            #endif /* EXAMPLE_CPP_COMPILER_HAS_MOVE_CONSTRUCTOR_DELETE */
        public:
            Initialization(const char* shared_library_name)
            {
                load_module(shared_library_name);
            }
            ~Initialization()
            {
                #ifdef _WIN32
                    FreeLibrary(handle);
                #else /* _WIN32 */
                    dlclose(handle);
                #endif /* _WIN32 */
                example_get_major_version = 0;
                example_get_minor_version = 0;
                example_get_patch_version = 0;
                example_printer_new = 0;
                example_printer_show = 0;
                example_printer_delete = 0;
                example_dumper_new = 0;
                example_dumper_get_printer = 0;
                example_dumper_set_printer = 0;
                example_dumper_dump = 0;
                example_dumper_copy = 0;
                example_dumper_delete = 0;
            }
        };
    }
    
    #endif /* __cplusplus */
    
#endif /* EXAMPLE_CAPI_USE_DYNAMIC_LOADER */

#endif /* EXAMPLE_CAPI_INCLUDED */

