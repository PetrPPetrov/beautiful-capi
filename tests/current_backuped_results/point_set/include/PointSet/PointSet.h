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

#ifndef POINTSET_POINTSET_DEFINITION_INCLUDED
#define POINTSET_POINTSET_DEFINITION_INCLUDED

#include "PointSet/PointSetDecl.h"
#include "PointSet/Points.h"

#ifdef __cplusplus

inline PointSet::PointSetPtr::PointSetPtr()
{
    SetObject(PointSet::PointSetPtr(PointSet::PointSetPtr::force_creating_from_raw_pointer, point_set_point_set_default(), false).Detach());
}

inline const char* PointSet::PointSetPtr::GetName() const
{
    return point_set_point_set_get_name_const(GetRawPointer());
}

inline void PointSet::PointSetPtr::SetName(const char* name)
{
    point_set_point_set_set_name(GetRawPointer(), name);
}

inline PointSet::PointsPtr PointSet::PointSetPtr::GetPoints() const
{
    return PointSet::PointsPtr(PointSet::PointsPtr::force_creating_from_raw_pointer, point_set_point_set_get_points_const(GetRawPointer()), false);
}

inline void PointSet::PointSetPtr::SetPoints(const PointSet::PointsPtr& value)
{
    point_set_point_set_set_points(GetRawPointer(), value.GetRawPointer());
}

inline PointSet::PointSetPtr::PointSetPtr(const PointSetPtr& other)
{
    SetObject(other.GetRawPointer());
    if (other.GetRawPointer())
    {
        point_set_point_set_add_ref(other.GetRawPointer());
    }
}

#ifdef POINTSET_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline PointSet::PointSetPtr::PointSetPtr(PointSetPtr&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* POINTSET_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline PointSet::PointSetPtr::PointSetPtr(PointSet::PointSetPtr::ECreateFromRawPointer, void *object_pointer, bool add_ref_object)
{
    SetObject(object_pointer);
    if (add_ref_object && object_pointer)
    {
        point_set_point_set_add_ref(object_pointer);
    }
}

inline PointSet::PointSetPtr::~PointSetPtr()
{
    if (GetRawPointer())
    {
        point_set_point_set_release(GetRawPointer());
        SetObject(0);
    }
}

inline PointSet::PointSetPtr& PointSet::PointSetPtr::operator=(const PointSet::PointSetPtr& other)
{
    if (GetRawPointer() != other.GetRawPointer())
    {
        if (GetRawPointer())
        {
            point_set_point_set_release(GetRawPointer());
            SetObject(0);
        }
        SetObject(other.GetRawPointer());
        if (other.GetRawPointer())
        {
            point_set_point_set_add_ref(other.GetRawPointer());
        }
    }
    return *this;
}

#ifdef POINTSET_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline PointSet::PointSetPtr& PointSet::PointSetPtr::operator=(PointSet::PointSetPtr&& other)
{
    if (GetRawPointer() != other.GetRawPointer())
    {
        if (GetRawPointer())
        {
            point_set_point_set_release(GetRawPointer());
            SetObject(0);
        }
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* POINTSET_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline PointSet::PointSetPtr PointSet::PointSetPtr::Null()
{
    return PointSet::PointSetPtr(PointSet::PointSetPtr::force_creating_from_raw_pointer, static_cast<void*>(0), false);
}

inline bool PointSet::PointSetPtr::IsNull() const
{
    return !GetRawPointer();
}

inline bool PointSet::PointSetPtr::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool PointSet::PointSetPtr::operator!() const
{
    return !GetRawPointer();
}

inline void* PointSet::PointSetPtr::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* PointSet::PointSetPtr::GetRawPointer() const
{
    return PointSet::PointSetPtr::mObject ? mObject: 0;
}

inline PointSet::PointSetPtr* PointSet::PointSetPtr::operator->()
{
    return this;
}

inline const PointSet::PointSetPtr* PointSet::PointSetPtr::operator->() const
{
    return this;
}

inline void PointSet::PointSetPtr::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* POINTSET_POINTSET_DEFINITION_INCLUDED */

