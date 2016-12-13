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

#ifndef EXAMPLE_MODEL_DOUBLE_DECLARATION_INCLUDED
#define EXAMPLE_MODEL_DOUBLE_DECLARATION_INCLUDED

#include "ExampleCapi.h"
#include "ExampleFwd.h"

#ifdef __cplusplus

namespace Example {

template<>
class ModelPtr<double>
{
public:
    inline ModelPtr();
    inline const char* GetName() const;
    inline void SetName(const char* name);
    inline Example::Position<double> GetPosition() const;
    inline void SetPosition(const Example::Position<double>& position);

    inline ModelPtr(const ModelPtr<double>& other);
    #ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline ModelPtr(ModelPtr<double>&& other);
    #endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    enum ECreateFromRawPointer { force_creating_from_raw_pointer };
    inline ModelPtr(ECreateFromRawPointer, void *object_pointer, bool add_ref_object);
    inline ~ModelPtr();
    inline ModelPtr<double>& operator=(const ModelPtr<double>& other);
    #ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
    inline ModelPtr<double>& operator=(ModelPtr<double>&& other);
    #endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */
    static inline ModelPtr<double> Null();
    inline bool IsNull() const;
    inline bool IsNotNull() const;
    inline bool operator!() const;
    inline void* Detach();
    inline void* GetRawPointer() const;
    inline ModelPtr<double>* operator->();
    inline const ModelPtr<double>* operator->() const;
protected:
    inline void SetObject(void* object_pointer);
    void* mObject;
};

}

#endif /* __cplusplus */

#endif /* EXAMPLE_MODEL_DOUBLE_DECLARATION_INCLUDED */

