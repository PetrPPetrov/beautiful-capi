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

#ifndef BEAUTIFUL_CAPI_DOXYGEN_DOC_PERSON_H
#define BEAUTIFUL_CAPI_DOXYGEN_DOC_PERSON_H

#include <iostream>
#include <vector>
#include <stddef.h>
#include "NameImpl.h"
#include "AddressImpl.h"

namespace DoxygenDoc
{
    class PersonImpl
    {
    public:
        PersonImpl(): mDay(0), mMonth(0), mYear(0), mName("", ""), mAddress(0) {}
        
        ~PersonImpl()
        {
            intrusive_ptr_release(mAddress);
        }

        DoxygenDoc::NameImpl GetName() const
        {
            return mName;
        }

        void SetName(DoxygenDoc::NameImpl name)
        {
            mName = name;
        }

        DoxygenDoc::AddressImpl* GetAddress() const
        {
            intrusive_ptr_add_ref(mAddress); // We return a raw pointer, so, we need to call AddRef() here
            return mAddress;
        }

        void SetAddress(DoxygenDoc::AddressImpl* address)
        {
            intrusive_ptr_add_ref(address);
            intrusive_ptr_release(mAddress);
            mAddress = address;
        }
        
        int GetDay() const
        {
            return mDay;
        }

        void SetDay(unsigned int day)
        {
            mDay = day;
        }

        int GetMonth() const
        {
            return mMonth;
        }

        void SetMonth(unsigned int month)
        {
            mMonth = month;
        }
        
        int GetYear() const
        {
            return mYear;
        }

        void SetYear(unsigned int year)
        {
            mYear = year;
        }

    private:
        DoxygenDoc::NameImpl mName;
        DoxygenDoc::AddressImpl* mAddress;
        unsigned mDay;
        unsigned mMonth;
        unsigned mYear;
    };
}

#endif /* BEAUTIFUL_CAPI_DOXYGEN_DOC_PERSON_H */
