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

#ifndef BEAUTIFUL_CAPI_UNIT_TEST_ADDRESS_H
#define BEAUTIFUL_CAPI_UNIT_TEST_ADDRESS_H

#include <string>
#include <iostream>
#include "snippets/UnitTest/PersonImpl.h"
#include "boost/smart_ptr/intrusive_ptr.hpp"

namespace UnitTest
{
    class AddressImpl
    {
        std::string mStreetName;
        std::string mCity;
        unsigned int mState;
        unsigned int mZipCode;
        
        int mRefCount;

    public:
        // By default newly created objects implies to have value 1 of reference counter
        AddressImpl() : mRefCount(1)
        {
            std::cout << "Address constructor" << std::endl;
        }
        // By default newly created objects implies to have value 1 of reference counter
        AddressImpl(const AddressImpl& other) 
            : mRefCount(1), mStreetName(other.mStreetName), mCity(other.mCity), mState(other.mState),
              mZipCode(other.mZipCode)
        {
            std::cout << "Address copy constructor! (should be never called)" << std::endl;
        }
        ~AddressImpl()
        {
            std::cout << "Address destructor" << std::endl;
        }

        const char* GetStreetName() const
        {
            return mStreetName.c_str();
        }

        void SetStreetName(const char* street_name)
        {
            mStreetName = street_name;
        }
        
        const char* GetCity() const
        {
            return mCity.c_str();
        }

        void SetCity(const char* city)
        {
            mCity = city;
        }
        
        unsigned int GetState() const
        {
            return mState;
        }

        void SetState(unsigned int state)
        {
            mState = state;
        }
        
        unsigned int GetZipCode() const
        {
            return mZipCode;
        }

        void SetZipCode(unsigned int zip_code)
        {
            mZipCode = zip_code;
        }

        void AddRef() 
        { 
            ++mRefCount;
        }
        void Release()
        {
            --mRefCount;
            if (mRefCount <= 0)
            {
                delete this;
            }
        }
    };

    inline void intrusive_ptr_add_ref(AddressImpl* object)
    {
        if (object)
        {
            object->AddRef();
        }
    }

    inline void intrusive_ptr_release(AddressImpl* object)
    {
        if (object)
        {
            object->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_UNIT_TEST_ADDRESS_H */
