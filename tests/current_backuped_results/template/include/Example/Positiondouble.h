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

#ifndef EXAMPLE_POSITION_DOUBLE_DEFINITION_INCLUDED
#define EXAMPLE_POSITION_DOUBLE_DEFINITION_INCLUDED

#include "Example/PositiondoubleDecl.h"

#ifdef __cplusplus

inline Example::Position<double>::Position()
{
    SetObject(example_position_double_default());
}

inline double Example::Position<double>::GetX() const
{
    return example_position_double_get_x(GetRawPointer());
}

inline void Example::Position<double>::SetX(double x)
{
    example_position_double_set_x(GetRawPointer(), x);
}

inline double Example::Position<double>::GetY() const
{
    return example_position_double_get_y(GetRawPointer());
}

inline void Example::Position<double>::SetY(double y)
{
    example_position_double_set_y(GetRawPointer(), y);
}

inline double Example::Position<double>::GetZ() const
{
    return example_position_double_get_z(GetRawPointer());
}

inline void Example::Position<double>::SetZ(double z)
{
    example_position_double_set_z(GetRawPointer(), z);
}

inline Example::Position<double>::Position(const Position<double>& other)
{
    if (other.GetRawPointer())
    {
        SetObject(example_position_double_copy(other.GetRawPointer()));
    }
    else
    {
        SetObject(0);
    }
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::Position<double>::Position(Position<double>&& other)
{
    mObject = other.GetRawPointer();
    other.mObject = 0;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::Position<double>::Position(Example::Position<double>::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        SetObject(example_position_double_copy(object_pointer));
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline Example::Position<double>::~Position()
{
    if (GetRawPointer())
    {
        example_position_double_delete(GetRawPointer());
        SetObject(0);
    }
}

inline Example::Position<double>& Example::Position<double>::operator=(const Example::Position<double>& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_position_double_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            SetObject(example_position_double_copy(other.GetRawPointer()));
        }
        else
        {
            SetObject(0);
        }
    }
    return *this;
}

#ifdef EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline Example::Position<double>& Example::Position<double>::operator=(Example::Position<double>&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            example_position_double_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.GetRawPointer();
        other.mObject = 0;
    }
    return *this;
}
#endif /* EXAMPLE_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline Example::Position<double> Example::Position<double>::Null()
{
    return Example::Position<double>(Example::Position<double>::force_creating_from_raw_pointer, 0, false);
}

inline bool Example::Position<double>::IsNull() const
{
    return !GetRawPointer();
}

inline bool Example::Position<double>::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool Example::Position<double>::operator!() const
{
    return !GetRawPointer();
}

inline void* Example::Position<double>::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* Example::Position<double>::GetRawPointer() const
{
    return Example::Position<double>::mObject ? mObject: 0;
}

inline void Example::Position<double>::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* EXAMPLE_POSITION_DOUBLE_DEFINITION_INCLUDED */

