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

#ifndef EXAMPLE_PRINTERCALLBACK_DECLARATION_INCLUDED
#define EXAMPLE_PRINTERCALLBACK_DECLARATION_INCLUDED

#include "ExampleCapi.h"
#include "ExampleFwd.h"
#include "Example/PrinterDecl.h"

#ifdef __cplusplus

namespace Example {

class PrinterCallbackPtr : public Example::PrinterPtr
{
public:
    inline PrinterCallbackPtr();
    inline void SetObjectPointer(void* custom_object);
    inline void* GetObjectPointer() const;
    inline void SetCFunctionForPrint(example_printer_print_const_callback_type c_function_pointer);
    inline void SetCFunctionForGetDeviceType(example_printer_get_device_type_const_callback_type c_function_pointer);
    inline void SetCFunctionForGetPrintingQuality(example_printer_get_printing_quality_const_callback_type c_function_pointer);
    inline void SetCFunctionForSetPrintingQuality(example_printer_set_printing_quality_callback_type c_function_pointer);

    inline PrinterCallbackPtr(const PrinterCallbackPtr& other);
    #ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline PrinterCallbackPtr(PrinterCallbackPtr&& other);
    #endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    enum ECreateFromRawPointer { force_creating_from_raw_pointer };
    inline PrinterCallbackPtr(ECreateFromRawPointer, void *object_pointer, bool add_ref_object);
    inline ~PrinterCallbackPtr();
    inline PrinterCallbackPtr& operator=(const PrinterCallbackPtr& other);
    #ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline PrinterCallbackPtr& operator=(PrinterCallbackPtr&& other);
    #endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    static inline PrinterCallbackPtr Null();
    inline bool IsNull() const;
    inline bool IsNotNull() const;
    inline bool operator!() const;
    inline void* Detach();
    inline void* GetRawPointer() const;
    inline PrinterCallbackPtr* operator->();
    inline const PrinterCallbackPtr* operator->() const;
protected:
    inline void SetObject(void* object_pointer);
    void* mObject;
};

template<typename ImplementationClass>
inline Example::PrinterCallbackPtr create_callback_for_printer(ImplementationClass* implementation_class);

template<typename ImplementationClass>
inline Example::PrinterCallbackPtr create_callback_for_printer(ImplementationClass& implementation_class);

}

namespace Example {

template<>
inline Example::PrinterCallbackPtr down_cast<Example::PrinterCallbackPtr >(const Example::PrinterPtr& source_object);

}

#endif /* __cplusplus */

#endif /* EXAMPLE_PRINTERCALLBACK_DECLARATION_INCLUDED */

