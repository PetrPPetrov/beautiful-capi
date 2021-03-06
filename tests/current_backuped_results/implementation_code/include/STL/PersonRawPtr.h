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

#ifndef STL_PERSONRAWPTR_DEFINITION_INCLUDED
#define STL_PERSONRAWPTR_DEFINITION_INCLUDED

#include "STL/PersonRawPtrDecl.h"
#include "ImplementationCode/common/check_and_throw_exception.h"
#include "STL/String.h"
#include "STL/PersonDecl.h"

#ifdef __cplusplus

inline STL::PersonRawPtr::PersonRawPtr()
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::PersonRawPtr result(STL::PersonRawPtr::force_creating_from_raw_pointer, stl_person_raw_ptr_default(&exception_info), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    SetObject(result.Detach());
}

inline unsigned int STL::PersonRawPtr::GetAge() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    unsigned int result(stl_person_raw_ptr_get_age_const(&exception_info, GetRawPointer()));
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::PersonRawPtr::SetAge(unsigned int age)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_raw_ptr_set_age(&exception_info, GetRawPointer(), age);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::String STL::PersonRawPtr::GetFirstName() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::String result(STL::String::force_creating_from_raw_pointer, stl_person_raw_ptr_get_first_name_const(&exception_info, GetRawPointer()), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::PersonRawPtr::SetFirstName(const STL::String& first_name)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_raw_ptr_set_first_name(&exception_info, GetRawPointer(), first_name.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::String STL::PersonRawPtr::GetSecondName() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::String result(STL::String::force_creating_from_raw_pointer, stl_person_raw_ptr_get_second_name_const(&exception_info, GetRawPointer()), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::PersonRawPtr::SetSecondName(const STL::String& second_name)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_person_raw_ptr_set_second_name(&exception_info, GetRawPointer(), second_name.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::PersonRawPtr::PersonRawPtr(const PersonRawPtr& other)
{
    SetObject(other.GetRawPointer());
}

#ifdef STL_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline STL::PersonRawPtr::PersonRawPtr(PersonRawPtr&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::PersonRawPtr::PersonRawPtr(STL::PersonRawPtr::ECreateFromRawPointer, void *object_pointer, bool)
{
    SetObject(object_pointer);
}

inline void STL::PersonRawPtr::Delete()
{
    if (GetRawPointer())
    {
        stl_person_raw_ptr_delete(GetRawPointer());
        SetObject(0);
    }
}

inline STL::PersonRawPtr& STL::PersonRawPtr::operator=(const STL::PersonRawPtr& other)
{
    if (this != &other)
    {
        SetObject(other.GetRawPointer());
    }
    return *this;
}

#ifdef STL_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline STL::PersonRawPtr& STL::PersonRawPtr::operator=(STL::PersonRawPtr&& other)
{
    if (this != &other)
    {
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::PersonRawPtr STL::PersonRawPtr::Null()
{
    return STL::PersonRawPtr(STL::PersonRawPtr::force_creating_from_raw_pointer, static_cast<void*>(0), false);
}

inline bool STL::PersonRawPtr::IsNull() const
{
    return !GetRawPointer();
}

inline bool STL::PersonRawPtr::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool STL::PersonRawPtr::operator!() const
{
    return !GetRawPointer();
}

inline void* STL::PersonRawPtr::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* STL::PersonRawPtr::GetRawPointer() const
{
    return STL::PersonRawPtr::mObject ? mObject: 0;
}

inline STL::PersonRawPtr* STL::PersonRawPtr::operator->()
{
    return this;
}

inline const STL::PersonRawPtr* STL::PersonRawPtr::operator->() const
{
    return this;
}

inline STL::PersonRawPtr::operator STL::Person() const
{
    return STL::Person(STL::Person::force_creating_from_raw_pointer, GetRawPointer(), true);
}

inline STL::PersonRawPtr::PersonRawPtr(const STL::Person& value)
{
    void* object_pointer = value.GetRawPointer();
    SetObject(object_pointer);
}


inline void STL::PersonRawPtr::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* STL_PERSONRAWPTR_DEFINITION_INCLUDED */

