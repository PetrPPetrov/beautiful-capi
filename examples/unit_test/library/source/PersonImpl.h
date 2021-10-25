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

#ifndef BEAUTIFUL_CAPI_UNIT_TEST_PERSON_H
#define BEAUTIFUL_CAPI_UNIT_TEST_PERSON_H

#include <iostream>
#include <vector>
#include <stddef.h>
#include "NameImpl.h"
#include "AddressImpl.h"

namespace UnitTest
{
#include "snippets/UnitTest.h"

    class PersonImpl
    {
    public:
        // By default newly created objects implies to have value 1 of reference counter
        PersonImpl()
            : mMother(0), mFather(0), mAge(0), mSex(Unknown), mName("", "", ""), mMaritalStatus(Single)
        {
            std::cout << "Person ctor" << std::endl;
        }
        // By default newly created objects implies to have value 1 of reference counter
        ~PersonImpl()
        {
            std::cout << "Person dtor" << std::endl;
        }

        UnitTest::NameImpl GetName() const
        {
            return mName;
        }

        void SetName(UnitTest::NameImpl name)
        {
            mName = name;
        }

        AddressImpl* GetAddress() const
        {
            mAddress->AddRef(); // We return a raw pointer, so, we need to call AddRef() here
            return mAddress.get();
        }

        void SetAddress(boost::intrusive_ptr<UnitTest::AddressImpl> address)
        {
            mAddress = address;
        }

        unsigned int GetAge() const
        {
            return mAge;
        }

        void SetAge(unsigned int age)
        {
            mAge = age;
        }

        Sex GetSex() const
        {
            return mSex;
        }

        void SetSex(Sex sex)
        {
            mSex = sex;
        }

        MaritalStatus GetMaritalStatus() const
        {
            return mMaritalStatus;
        }

        void SetMaritalStatus(MaritalStatus marital_status)
        {
            mMaritalStatus = marital_status;
        }

        PersonImpl* GetMother() const
        {
            return mMother;
        }

        void SetMother(PersonImpl* mother)
        {
            mMother = mother;
        }

        PersonImpl* GetFather()  const
        {
            return mFather;
        }

        void SetFather(PersonImpl* father)
        {
            mFather = father;
        }

    private:
        UnitTest::NameImpl mName;
        boost::intrusive_ptr<UnitTest::AddressImpl> mAddress;
        unsigned char mAge;
        Sex mSex;
        MaritalStatus mMaritalStatus;
        PersonImpl* mMother;
        PersonImpl* mFather;
    };
}

#endif /* BEAUTIFUL_CAPI_UNIT_TEST_PERSON_H */
