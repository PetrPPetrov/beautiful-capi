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

#ifndef BEAUTIFUL_CAPI_RETURN_VALUE_PERSON_H
#define BEAUTIFUL_CAPI_RETURN_VALUE_PERSON_H

#include <iostream>
#include <vector>
#include <stddef.h>

namespace ReturnValue
{
    class PersonImpl
    {
    private:
        ReturnValue::FirstNameImpl mFirstName;
        ReturnValue::MiddleNameImpl* mMiddleName;
        ReturnValue::LastNameImpl* mLastName; 
        
    public:
        PersonImpl() {}

        ReturnValue::FirstNameImpl GetFirstName() const
        {
            return mFirstName;
        }

        void SetFirstName(ReturnValue::FirstNameImpl first_name)
        {
            mFirstName = first_name;
        }

        ReturnValue::MiddleNameImpl* GetMiddleName() const
        {
            return mMiddleName;
        }

        void SetMiddleName(ReturnValue::MiddleNameImpl* middle_name)
        {
            intrusive_ptr_add_ref(middle_name);
            intrusive_ptr_release(mMiddleName);
            mMiddleName = middle_name;
        }
                
        ReturnValue::LastNameImpl* GetLastName() const
        {
            return mLastName;
        }

        void SetLastName(ReturnValue::LastNameImpl* last_name)
        {
            mLastName = last_name;
        }
    };
}

#endif /* BEAUTIFUL_CAPI_RETURN_VALUE_PERSON_H */
