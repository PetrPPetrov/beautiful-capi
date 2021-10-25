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

#ifndef BEAUTIFUL_CAPI_PERSON_H
#define BEAUTIFUL_CAPI_PERSON_H

#include <string>
#include <iostream>

namespace Example
{
#include "snippets/Example.h"

    class PersonImpl
    {
    private:
        std::string first_name;
        std::string last_name;
        unsigned int age;
        Example::ESex sex;
    public:
        PersonImpl();
        PersonImpl(const PersonImpl& other);
        ~PersonImpl();
        void SetFirstName(const char* first_name);
        const char* GetFirstName() const;
        void SetLastName(const char* last_name);
        const char* GetLastName() const;
        void SetAge(unsigned int age);
        unsigned int GetAge() const;
        void SetSex(Example::ESex sex);
        Example::ESex GetSex() const;
    };
}

#endif /* BEAUTIFUL_CAPI_PERSON_H */
