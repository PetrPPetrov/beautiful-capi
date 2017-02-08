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

#ifndef BEAUTIFUL_CAPI_UNIT_TEST_NAME_H
#define BEAUTIFUL_CAPI_UNIT_TEST_NAME_H

#include <iostream>
#include <sstream>

namespace UnitTest
{
    class NameImpl
    {
        std::string mFirstName;
        std::string mMiddleName;
        std::string mLastName;
        
        void init_from_char(const char* value, std::string &result_string)
        {
            if (value != nullptr)
                result_string = value;
        }
    public:
        NameImpl(const char* first_name, const char* middle_name, const char* last_name) 
        {
            std::cout << "Name ctor" << std::endl;
            init_from_char(first_name, mFirstName);
            init_from_char(middle_name, mMiddleName);
            init_from_char(last_name, mLastName);
        }

        ~NameImpl()
        {
            std::cout << "Name dtor" << std::endl;
        }

        const char* GetFullName() const
        {
            std::stringstream result;
            result << mFirstName << " " << mMiddleName << " " << mLastName;
            return result.str().c_str();
        }

        const char* GetFirstName() const
        { 
            return mFirstName.c_str(); 
        }

        const char* GetMiddleName() const
        {
            return mMiddleName.c_str();
        }

        const char* GetLastName() const
        {
            return mLastName.c_str();
        }

        void SetFirstName(const char* value)
        {
            mFirstName = value;
        }

        void SetMiddleName(const char* value)
        {
            mMiddleName = value;
        }

        void SetLastName(const char* value)
        {
            mLastName = value;
        }
    };
}

#endif /* BEAUTIFUL_CAPI_UNIT_TEST_NAME_H */
