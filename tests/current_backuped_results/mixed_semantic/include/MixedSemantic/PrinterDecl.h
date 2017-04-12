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

#ifndef MIXEDSEMANTIC_PRINTER_DECLARATION_INCLUDED
#define MIXEDSEMANTIC_PRINTER_DECLARATION_INCLUDED

#include "MixedSemanticCapi.h"
#include "MixedSemanticFwd.h"

#ifdef __cplusplus

namespace MixedSemantic {

class Printer
{
public:
    inline Printer();
    inline void Show(const MixedSemantic::Name& name);
    inline void ShowByPointer(const MixedSemantic::Name& name);
    inline void ShowByReference(const MixedSemantic::Name& name);
    inline void Show(const MixedSemantic::PersonRawPtr& person);
    inline void ShowByPointer(const MixedSemantic::PersonRawPtr& person);
    inline void ShowByReference(const MixedSemantic::PersonRawPtr& person);
    inline void Show(const MixedSemantic::AddressPtr& address);
    inline void ShowByPointer(const MixedSemantic::AddressPtr& address);
    inline void ShowByReference(const MixedSemantic::AddressPtr& address);

    inline Printer(const Printer& other);
    #ifdef MIXEDSEMANTIC_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline Printer(Printer&& other);
    #endif /* MIXEDSEMANTIC_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    enum ECreateFromRawPointer { force_creating_from_raw_pointer };
    inline Printer(ECreateFromRawPointer, void *object_pointer, bool copy_object);
    inline ~Printer();
    inline Printer& operator=(const Printer& other);
    #ifdef MIXEDSEMANTIC_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline Printer& operator=(Printer&& other);
    #endif /* MIXEDSEMANTIC_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    static inline Printer Null();
    inline bool IsNull() const;
    inline bool IsNotNull() const;
    inline bool operator!() const;
    inline void* Detach();
    inline void* GetRawPointer() const;
protected:
    inline void SetObject(void* object_pointer);
    void* mObject;
};

}

#endif /* __cplusplus */

#endif /* MIXEDSEMANTIC_PRINTER_DECLARATION_INCLUDED */
