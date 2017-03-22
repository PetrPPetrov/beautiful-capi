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

#ifndef MAPPEDTYPES_PERSON_DEFINITION_INCLUDED
#define MAPPEDTYPES_PERSON_DEFINITION_INCLUDED

#include "MappedTypes/PersonDecl.h"

#ifdef __cplusplus

inline MappedTypes::Person::Person()
{
    SetObject(mapped_types_person_default());
}

inline bool MappedTypes::Person::IsMan() const
{
    return (mapped_types_person_is_man_const(GetRawPointer()) ? true : false);
}

inline void MappedTypes::Person::SetSex(bool Sex)
{
    mapped_types_person_set_sex(GetRawPointer(), static_cast<uint8_t>(Sex));
}

inline int32_t MappedTypes::Person::GetAge() const
{
    return static_cast<int32_t>(mapped_types_person_get_age_const(GetRawPointer()));
}

inline void MappedTypes::Person::SetAge(int32_t age)
{
    mapped_types_person_set_age(GetRawPointer(), static_cast<int32_t>(age));
}

inline std::string MappedTypes::Person::GetFirstName() const
{
    return std::string(mapped_types_person_get_first_name_const(GetRawPointer()));
}

inline void MappedTypes::Person::SetFirstName(const std::string& first_name)
{
    mapped_types_person_set_first_name(GetRawPointer(), first_name.c_str());
}

inline std::string MappedTypes::Person::GetSecondName() const
{
    return std::string(mapped_types_person_get_second_name_const(GetRawPointer()));
}

inline void MappedTypes::Person::SetSecondName(const std::string& second_name)
{
    mapped_types_person_set_second_name(GetRawPointer(), second_name.c_str());
}

inline MappedTypes::Person::Person(const Person& other)
{
    if (other.GetRawPointer())
    {
        SetObject(mapped_types_person_copy(other.GetRawPointer()));
    }
    else
    {
        SetObject(0);
    }
}

#ifdef MAPPEDTYPES_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline MappedTypes::Person::Person(Person&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* MAPPEDTYPES_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline MappedTypes::Person::Person(MappedTypes::Person::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        SetObject(mapped_types_person_copy(object_pointer));
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline MappedTypes::Person::~Person()
{
    if (GetRawPointer())
    {
        mapped_types_person_delete(GetRawPointer());
        SetObject(0);
    }
}

inline MappedTypes::Person& MappedTypes::Person::operator=(const MappedTypes::Person& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            mapped_types_person_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            SetObject(mapped_types_person_copy(other.mObject));
        }
        else
        {
            SetObject(0);
        }
    }
    return *this;
}

#ifdef MAPPEDTYPES_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline MappedTypes::Person& MappedTypes::Person::operator=(MappedTypes::Person&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            mapped_types_person_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* MAPPEDTYPES_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline MappedTypes::Person MappedTypes::Person::Null()
{
    return MappedTypes::Person(MappedTypes::Person::force_creating_from_raw_pointer, 0, false);
}

inline bool MappedTypes::Person::IsNull() const
{
    return !GetRawPointer();
}

inline bool MappedTypes::Person::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool MappedTypes::Person::operator!() const
{
    return !GetRawPointer();
}

inline void* MappedTypes::Person::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* MappedTypes::Person::GetRawPointer() const
{
    return MappedTypes::Person::mObject ? mObject: 0;
}

inline void MappedTypes::Person::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* MAPPEDTYPES_PERSON_DEFINITION_INCLUDED */

