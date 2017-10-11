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

#ifndef STL_PERSON_DEFINITION_INCLUDED
#define STL_PERSON_DEFINITION_INCLUDED

#include "STL/PersonDecl.h"
#include "ImplementationCode/common/check_and_throw_exception.h"
#include "STL/String.h"

#ifdef __cplusplus

inline STL::Person::Person()
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::Person result(STL::Person::force_creating_from_raw_pointer, stl_person_default(&exception_info), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    SetObject(result.Detach());
}

inline unsigned int STL::Person::GetAge() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    unsigned int result(stl_person_get_age_const(&exception_info, GetRawPointer()));
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::Person::SetAge(unsigned int age)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_set_age(&exception_info, GetRawPointer(), age);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::String STL::Person::GetFirstName() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::String result(STL::String::force_creating_from_raw_pointer, stl_person_get_first_name_const(&exception_info, GetRawPointer()), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::Person::SetFirstName(const STL::String& first_name)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_set_first_name(&exception_info, GetRawPointer(), first_name.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::String STL::Person::GetSecondName() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::String result(STL::String::force_creating_from_raw_pointer, stl_person_get_second_name_const(&exception_info, GetRawPointer()), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::Person::SetSecondName(const STL::String& second_name)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_set_second_name(&exception_info, GetRawPointer(), second_name.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::Person::Person(const Person& other)
{
    if (other.GetRawPointer())
    {
        beautiful_capi_implementationcode_exception_info_t exception_info;
        void* result(stl_person_copy(&exception_info, other.GetRawPointer()));
        beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
        SetObject(result);
    }
    else
    {
        SetObject(0);
    }
}

#ifdef STL_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline STL::Person::Person(Person&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::Person::Person(STL::Person::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        beautiful_capi_implementationcode_exception_info_t exception_info;
        void* result(stl_person_copy(&exception_info, object_pointer));
        beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
        SetObject(result);
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline STL::Person::~Person()
{
    if (GetRawPointer())
    {
        stl_person_delete(GetRawPointer());
        SetObject(0);
    }
}

inline STL::Person& STL::Person::operator=(const STL::Person& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            stl_person_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            beautiful_capi_implementationcode_exception_info_t exception_info;
            void* result(stl_person_copy(&exception_info, other.mObject));
            beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
            SetObject(result);
        }
        else
        {
            SetObject(0);
        }
    }
    return *this;
}

#ifdef STL_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline STL::Person& STL::Person::operator=(STL::Person&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            stl_person_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::Person STL::Person::Null()
{
    return STL::Person(STL::Person::force_creating_from_raw_pointer, static_cast<void*>(0), false);
}

inline bool STL::Person::IsNull() const
{
    return !GetRawPointer();
}

inline bool STL::Person::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool STL::Person::operator!() const
{
    return !GetRawPointer();
}

inline void* STL::Person::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* STL::Person::GetRawPointer() const
{
    return STL::Person::mObject ? mObject: 0;
}

inline void STL::Person::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* STL_PERSON_DEFINITION_INCLUDED */
