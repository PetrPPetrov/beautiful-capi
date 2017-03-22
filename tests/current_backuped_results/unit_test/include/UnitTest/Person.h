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

#ifndef UNITTEST_PERSON_DEFINITION_INCLUDED
#define UNITTEST_PERSON_DEFINITION_INCLUDED

#include "UnitTest/PersonDecl.h"
#include "UnitTest/Name.h"
#include "UnitTest/Address.h"
#include "UnitTest/Person.h"

#ifdef __cplusplus

inline UnitTest::PersonRawPtr::PersonRawPtr()
{
    SetObject(unit_test_person_default());
}

inline UnitTest::Name UnitTest::PersonRawPtr::GetName() const
{
    return UnitTest::Name(UnitTest::Name::force_creating_from_raw_pointer, unit_test_person_get_name_const(GetRawPointer()), false);
}

inline void UnitTest::PersonRawPtr::SetName(const UnitTest::Name& value)
{
    unit_test_person_set_name(GetRawPointer(), value.GetRawPointer());
}

inline UnitTest::AddressPtr UnitTest::PersonRawPtr::GetAddress() const
{
    return UnitTest::AddressPtr(UnitTest::AddressPtr::force_creating_from_raw_pointer, unit_test_person_get_address_const(GetRawPointer()), false);
}

inline void UnitTest::PersonRawPtr::SetAddress(const UnitTest::AddressPtr& value)
{
    unit_test_person_set_address(GetRawPointer(), value.GetRawPointer());
}

inline unsigned char UnitTest::PersonRawPtr::GetAge() const
{
    return unit_test_person_get_age_const(GetRawPointer());
}

inline void UnitTest::PersonRawPtr::SetAge(unsigned char value)
{
    unit_test_person_set_age(GetRawPointer(), value);
}

inline UnitTest::PersonRawPtr::Sex UnitTest::PersonRawPtr::GetSex() const
{
    return UnitTest::PersonRawPtr::Sex(static_cast<UnitTest::PersonRawPtr::Sex>(unit_test_person_get_sex_const(GetRawPointer())));
}

inline void UnitTest::PersonRawPtr::SetSex(UnitTest::PersonRawPtr::Sex value)
{
    unit_test_person_set_sex(GetRawPointer(), static_cast<unsigned int>(value));
}

inline UnitTest::PersonRawPtr UnitTest::PersonRawPtr::GetMother() const
{
    return UnitTest::PersonRawPtr(UnitTest::PersonRawPtr::force_creating_from_raw_pointer, unit_test_person_get_mother_const(GetRawPointer()), false);
}

inline void UnitTest::PersonRawPtr::SetMother(const UnitTest::PersonRawPtr& value)
{
    unit_test_person_set_mother(GetRawPointer(), value.GetRawPointer());
}

inline UnitTest::PersonRawPtr UnitTest::PersonRawPtr::GetFather() const
{
    return UnitTest::PersonRawPtr(UnitTest::PersonRawPtr::force_creating_from_raw_pointer, unit_test_person_get_father_const(GetRawPointer()), false);
}

inline void UnitTest::PersonRawPtr::SetFather(const UnitTest::PersonRawPtr& value)
{
    unit_test_person_set_father(GetRawPointer(), value.GetRawPointer());
}

inline UnitTest::PersonRawPtr::PersonRawPtr(const PersonRawPtr& other)
{
    SetObject(other.GetRawPointer());
}

#ifdef UNITTEST_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline UnitTest::PersonRawPtr::PersonRawPtr(PersonRawPtr&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* UNITTEST_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline UnitTest::PersonRawPtr::PersonRawPtr(UnitTest::PersonRawPtr::ECreateFromRawPointer, void *object_pointer, bool)
{
    SetObject(object_pointer);
}

inline void UnitTest::PersonRawPtr::Delete()
{
    if (GetRawPointer())
    {
        unit_test_person_delete(GetRawPointer());
        SetObject(0);
    }
}

inline UnitTest::PersonRawPtr& UnitTest::PersonRawPtr::operator=(const UnitTest::PersonRawPtr& other)
{
    if (this != &other)
    {
        SetObject(other.GetRawPointer());
    }
    return *this;
}

#ifdef UNITTEST_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline UnitTest::PersonRawPtr& UnitTest::PersonRawPtr::operator=(UnitTest::PersonRawPtr&& other)
{
    if (this != &other)
    {
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* UNITTEST_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline UnitTest::PersonRawPtr UnitTest::PersonRawPtr::Null()
{
    return UnitTest::PersonRawPtr(UnitTest::PersonRawPtr::force_creating_from_raw_pointer, 0, false);
}

inline bool UnitTest::PersonRawPtr::IsNull() const
{
    return !GetRawPointer();
}

inline bool UnitTest::PersonRawPtr::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool UnitTest::PersonRawPtr::operator!() const
{
    return !GetRawPointer();
}

inline void* UnitTest::PersonRawPtr::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* UnitTest::PersonRawPtr::GetRawPointer() const
{
    return UnitTest::PersonRawPtr::mObject ? mObject: 0;
}

inline UnitTest::PersonRawPtr* UnitTest::PersonRawPtr::operator->()
{
    return this;
}

inline const UnitTest::PersonRawPtr* UnitTest::PersonRawPtr::operator->() const
{
    return this;
}

inline void UnitTest::PersonRawPtr::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* UNITTEST_PERSON_DEFINITION_INCLUDED */
