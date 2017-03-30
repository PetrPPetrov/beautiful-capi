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

#ifndef BEAUTIFUL_CAPI_MIXED_SEMANTIC2_NAME_H
#define BEAUTIFUL_CAPI_MIXED_SEMANTIC2_NAME_H

#include <iostream>
#include <string>
#include <sstream>

namespace MixedSemantic2
{
    class NameImpl
    {
        std::string mFirstName;
        std::string mFatherName;        
        std::string mLastName;

        void init_from_char(const char* value, std::string &result_string)
        {
            if (value)
                result_string = value;
        }
    public:
        NameImpl(const char* first_name, const char* father_name, const char* last_name) 
        {
            init_from_char(first_name, mFirstName);
            init_from_char(father_name, mFatherName);
            init_from_char(last_name, mLastName);
        }

        const char* GetFirstName() const
        {
            return mFirstName.c_str();
        }

        const char* GetLastName() const
        {
            return mLastName.c_str();
        }

        const char* GetFatherName() const
        {
            return mFatherName.c_str();
        }

        void SetFirstName(const char* value)
        {
            mFirstName = value;
        }

        void SetLastName(const char* value)
        {
            mLastName = value;
        }

        void SetFatherName(const char* value)
        {
            mFatherName = value;
        }
    };
}

#endif /* BEAUTIFUL_CAPI_MIXED_SEMANTIC2_NAME_H */
