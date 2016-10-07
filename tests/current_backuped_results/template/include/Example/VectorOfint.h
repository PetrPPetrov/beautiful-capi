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

#ifndef EXAMPLE_VECTOROF_INT_DEFINITION_INCLUDED
#define EXAMPLE_VECTOROF_INT_DEFINITION_INCLUDED

#include "Example/VectorOfintDecl.h"

#ifdef __cplusplus

inline Example::VectorOf<int>::VectorOf()
{
    SetObject(example_vector_of_int_default());
}

inline int Example::VectorOf<int>::GetSize() const
{
    return example_vector_of_int_get_size(GetRawPointer());
}

inline void Example::VectorOf<int>::Clear()
{
    example_vector_of_int_clear(GetRawPointer());
}

inline void Example::VectorOf<int>::PushBack(int value)
{
    example_vector_of_int_push_back(GetRawPointer(), value);
}

inline int Example::VectorOf<int>::GetItem(int index) const
{
    return example_vector_of_int_get_item(GetRawPointer(), index);
}

inline Example::VectorOf<int>::VectorOf(const VectorOf<int>& other)
{
    if (other.GetRawPointer())
    {
        SetObject(example_vector_of_int_copy(other.GetRawPointer()));
    }
    else
    {
        SetObject(0);
    }
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::VectorOf<int>::VectorOf(VectorOf<int>&& other)
{
    mObject = other.GetRawPointer();
    other.mObject = 0;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::VectorOf<int>::VectorOf(Example::VectorOf<int>::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        SetObject(example_vector_of_int_copy(object_pointer));
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline Example::VectorOf<int>::~VectorOf()
{
    if (GetRawPointer())
    {
        example_vector_of_int_delete(GetRawPointer());
        SetObject(0);
    }
}

inline Example::VectorOf<int>& Example::VectorOf<int>::operator=(const Example::VectorOf<int>& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_vector_of_int_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            SetObject(example_vector_of_int_copy(other.GetRawPointer()));
        }
        else
        {
            SetObject(0);
        }
    }
    return *this;
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::VectorOf<int>& Example::VectorOf<int>::operator=(Example::VectorOf<int>&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_vector_of_int_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.GetRawPointer();
        other.mObject = 0;
    }
    return *this;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::VectorOf<int> Example::VectorOf<int>::Null()
{
    return Example::VectorOf<int>(Example::VectorOf<int>::force_creating_from_raw_pointer, 0, false);
}

inline bool Example::VectorOf<int>::IsNull() const
{
    return !GetRawPointer();
}

inline bool Example::VectorOf<int>::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool Example::VectorOf<int>::operator!() const
{
    return !GetRawPointer();
}

inline void* Example::VectorOf<int>::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* Example::VectorOf<int>::GetRawPointer() const
{
    return Example::VectorOf<int>::mObject ? mObject: 0;
}

inline void Example::VectorOf<int>::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* EXAMPLE_VECTOROF_INT_DEFINITION_INCLUDED */

