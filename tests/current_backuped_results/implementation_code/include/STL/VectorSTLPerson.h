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

#ifndef STL_VECTOR_STL_PERSON_DEFINITION_INCLUDED
#define STL_VECTOR_STL_PERSON_DEFINITION_INCLUDED

#include "STL/VectorSTLPersonDecl.h"
#include "ImplementationCode/common/check_and_throw_exception.h"
#include "STL/Person.h"

#ifdef __cplusplus

inline STL::Vector<STL::Person>::Vector()
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::Vector<STL::Person> result(STL::Vector<STL::Person>::force_creating_from_raw_pointer, stl_vector_stl_person_default(&exception_info), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    SetObject(result.Detach());
}

inline size_t STL::Vector<STL::Person>::GetSize() const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    size_t result(stl_vector_stl_person_get_size_const(&exception_info, GetRawPointer()));
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline STL::Person STL::Vector<STL::Person>::GetElement(size_t index) const
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    STL::Person result(STL::Person::force_creating_from_raw_pointer, stl_vector_stl_person_get_element_const(&exception_info, GetRawPointer(), index), false);
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}

inline void STL::Vector<STL::Person>::SetElement(size_t index, const STL::Person& value)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_vector_stl_person_set_element(&exception_info, GetRawPointer(), index, value.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline void STL::Vector<STL::Person>::PushBack(const STL::Person& value)
{
    beautiful_capi_implementationcode_exception_info_t exception_info;
    stl_vector_stl_person_push_back(&exception_info, GetRawPointer(), value.GetRawPointer());
    beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
}

inline STL::Vector<STL::Person>::Vector(const Vector<STL::Person>& other)
{
    if (other.GetRawPointer())
    {
        beautiful_capi_implementationcode_exception_info_t exception_info;
        void* result(stl_vector_stl_person_copy(&exception_info, other.GetRawPointer()));
        beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
        SetObject(result);
    }
    else
    {
        SetObject(0);
    }
}

#ifdef STL_CPP_COMPILER_HAS_RVALUE_REFERENCES
inline STL::Vector<STL::Person>::Vector(Vector<STL::Person>&& other)
{
    mObject = other.mObject;
    other.mObject = 0;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::Vector<STL::Person>::Vector(STL::Vector<STL::Person>::ECreateFromRawPointer, void *object_pointer, bool copy_object)
{
    if (object_pointer && copy_object)
    {
        beautiful_capi_implementationcode_exception_info_t exception_info;
        void* result(stl_vector_stl_person_copy(&exception_info, object_pointer));
        beautiful_capi_ImplementationCode::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
        SetObject(result);
    }
    else
    {
        SetObject(object_pointer);
    }
}

inline STL::Vector<STL::Person>::~Vector()
{
    if (GetRawPointer())
    {
        stl_vector_stl_person_delete(GetRawPointer());
        SetObject(0);
    }
}

inline STL::Vector<STL::Person>& STL::Vector<STL::Person>::operator=(const STL::Vector<STL::Person>& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            stl_vector_stl_person_delete(GetRawPointer());
            SetObject(0);
        }
        if (other.GetRawPointer())
        {
            beautiful_capi_implementationcode_exception_info_t exception_info;
            void* result(stl_vector_stl_person_copy(&exception_info, other.mObject));
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
inline STL::Vector<STL::Person>& STL::Vector<STL::Person>::operator=(STL::Vector<STL::Person>&& other)
{
    if (this != &other)
    {
        if (GetRawPointer())
        {
            stl_vector_stl_person_delete(GetRawPointer());
            SetObject(0);
        }
        mObject = other.mObject;
        other.mObject = 0;
    }
    return *this;
}
#endif /* STL_CPP_COMPILER_HAS_RVALUE_REFERENCES */

inline STL::Vector<STL::Person> STL::Vector<STL::Person>::Null()
{
    return STL::Vector<STL::Person>(STL::Vector<STL::Person>::force_creating_from_raw_pointer, static_cast<void*>(0), false);
}

inline bool STL::Vector<STL::Person>::IsNull() const
{
    return !GetRawPointer();
}

inline bool STL::Vector<STL::Person>::IsNotNull() const
{
    return GetRawPointer() != 0;
}

inline bool STL::Vector<STL::Person>::operator!() const
{
    return !GetRawPointer();
}

inline void* STL::Vector<STL::Person>::Detach()
{
    void* result = GetRawPointer();
    SetObject(0);
    return result;
}

inline void* STL::Vector<STL::Person>::GetRawPointer() const
{
    return STL::Vector<STL::Person>::mObject ? mObject: 0;
}

inline void STL::Vector<STL::Person>::SetObject(void* object_pointer)
{
    mObject = object_pointer;
}

#endif /* __cplusplus */

#endif /* STL_VECTOR_STL_PERSON_DEFINITION_INCLUDED */

