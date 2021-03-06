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

#ifndef EXAMPLE_ISQUARE_DEFINITION_INCLUDED
#define EXAMPLE_ISQUARE_DEFINITION_INCLUDED

#include "Example/ISquareDecl.h"
#include "Example/IPolygon.h"

#ifdef __cplusplus

inline void Example::ISquarePtr::SetSize(double size)
{
    example_isquare_set_size(GetRawPointer(), size);
}

inline Example::ISquarePtr::ISquarePtr(const ISquarePtr& other) : Example::IPolygonPtr(Example::IPolygonPtr::force_creating_from_raw_pointer, static_cast<void*>(0), false)
{
    SetObject(other.GetRawPointer());
    if (other.GetRawPointer())
    {
        example_isquare_add_ref(other.GetRawPointer());
    }
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::ISquarePtr::ISquarePtr(ISquarePtr&& other) : Example::IPolygonPtr(std::move(other))
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::ISquarePtr::ISquarePtr(Example::ISquarePtr::ECreateFromRawPointer, void *object_pointer, bool add_ref_object) : Example::IPolygonPtr(Example::IPolygonPtr::force_creating_from_raw_pointer, static_cast<void*>(0), false)
{
    SetObject(object_pointer);
    if (add_ref_object && object_pointer)
    {
        example_isquare_add_ref(object_pointer);
    }
}

inline Example::ISquarePtr::~ISquarePtr()
{
    if (GetRawPointer())
    {
        example_isquare_release(GetRawPointer());
        SetObject(0);
    }
}

inline Example::ISquarePtr& Example::ISquarePtr::operator=(const Example::ISquarePtr& other)
{
    if (GetRawPointer() != other.GetRawPointer())
    {
        if (GetRawPointer())
        {
            example_isquare_release(GetRawPointer());
            SetObject(0);
        }
        SetObject(other.GetRawPointer());
        if (other.GetRawPointer())
        {
            example_isquare_add_ref(other.GetRawPointer());
        }
    }
    return *this;
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::ISquarePtr& Example::ISquarePtr::operator=(Example::ISquarePtr&& other)
{
    if (GetRawPointer() != other.GetRawPointer())
    {
        if (GetRawPointer())
        {
            example_isquare_release(GetRawPointer());
            SetObject(0);
        }
        Example::IPolygonPtr::operator=(std::move(other));
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::ISquarePtr Example::ISquarePtr::Null()
{
    return Example::ISquarePtr(Example::ISquarePtr::force_creating_from_raw_pointer, static_cast<void*>(0), false);
}

inline bool Example::ISquarePtr::IsNull() const
{
    return !GetRawPointer();
}

inline bool Example::ISquarePtr::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool Example::ISquarePtr::operator!() const
{
    return !GetRawPointer();
}

inline void* Example::ISquarePtr::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* Example::ISquarePtr::GetRawPointer() const
{
    return Example::IShapePtr::mObject ? mObject: 0;
}

inline Example::ISquarePtr* Example::ISquarePtr::operator->()
{
    return this;
}

inline const Example::ISquarePtr* Example::ISquarePtr::operator->() const
{
    return this;
}

inline void Example::ISquarePtr::SetObject(void* object_pointer)
{
    mObject = object_pointer;
    if (mObject)
    {
        Example::IPolygonPtr::SetObject(example_isquare_cast_to_base(mObject));
    }
    else
    {
        Example::IPolygonPtr::SetObject(0);
    }
}

namespace Example {

template<>
inline Example::ISquarePtr down_cast<Example::ISquarePtr >(const Example::IShapePtr& source_object)
{
    return Example::ISquarePtr(Example::ISquarePtr::force_creating_from_raw_pointer, example_ishape_cast_to_example_isquare(source_object.GetRawPointer()), true);
}

}

namespace Example {

template<>
inline Example::ISquarePtr down_cast<Example::ISquarePtr >(const Example::IPolygonPtr& source_object)
{
    return Example::ISquarePtr(Example::ISquarePtr::force_creating_from_raw_pointer, example_ipolygon_cast_to_example_isquare(source_object.GetRawPointer()), true);
}

}

#endif /* __cplusplus */

#endif /* EXAMPLE_ISQUARE_DEFINITION_INCLUDED */

