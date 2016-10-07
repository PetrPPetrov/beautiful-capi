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

#ifndef EXAMPLE_GEOMETRY_BREP_BODY_DEFINITION_INCLUDED
#define EXAMPLE_GEOMETRY_BREP_BODY_DEFINITION_INCLUDED

#include "Example/Geometry/Brep/BodyDecl.h"

#ifdef __cplusplus

inline Example::Geometry::Brep::Body::Body()
{
    SetObject(example_geometry_brep_body_new());
}

inline const char* Example::Geometry::Brep::Body::GetName()
{
    return example_geometry_brep_body_get_name(GetRawPointer());
}

inline void Example::Geometry::Brep::Body::SetName(const char* value)
{
    example_geometry_brep_body_set_name(GetRawPointer(), value);
}

inline Example::Geometry::Brep::Body::Body(const Body& other)
{
    if (other.GetRawPointer())
    {
        SetObject(example_geometry_brep_body_copy(other.GetRawPointer()));
    }
    else
    {
        SetObject(0);
    }
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::Geometry::Brep::Body::Body(Body&& other)
{
    mObject = other.GetRawPointer();
    other.mObject = 0;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::Geometry::Brep::Body::Body(Example::Geometry::Brep::Body::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        SetObject(example_geometry_brep_body_copy(object_pointer));
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline Example::Geometry::Brep::Body::~Body()
{
    if (GetRawPointer())
    {
        example_geometry_brep_body_delete(GetRawPointer());
        SetObject(0);
    }
}

inline Example::Geometry::Brep::Body& Example::Geometry::Brep::Body::operator=(const Example::Geometry::Brep::Body& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_geometry_brep_body_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            SetObject(example_geometry_brep_body_copy(other.GetRawPointer()));
        }
        else
        {
            SetObject(0);
        }
    }
    return *this;
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::Geometry::Brep::Body& Example::Geometry::Brep::Body::operator=(Example::Geometry::Brep::Body&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_geometry_brep_body_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.GetRawPointer();
        other.mObject = 0;
    }
    return *this;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::Geometry::Brep::Body Example::Geometry::Brep::Body::Null()
{
    return Example::Geometry::Brep::Body(Example::Geometry::Brep::Body::force_creating_from_raw_pointer, 0, false);
}

inline bool Example::Geometry::Brep::Body::IsNull() const
{
    return !GetRawPointer();
}

inline bool Example::Geometry::Brep::Body::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool Example::Geometry::Brep::Body::operator!() const
{
    return !GetRawPointer();
}

inline void* Example::Geometry::Brep::Body::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* Example::Geometry::Brep::Body::GetRawPointer() const
{
    return Example::Geometry::Brep::Body::mObject ? mObject: 0;
}

inline void Example::Geometry::Brep::Body::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* EXAMPLE_GEOMETRY_BREP_BODY_DEFINITION_INCLUDED */

