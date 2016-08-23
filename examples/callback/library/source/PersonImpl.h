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
#include "IPrinter.h"

namespace Example
{
    class PersonImpl
    {
        std::string first_name;
        std::string second_name;
        unsigned int age;
        bool male;
    public:
        PersonImpl();
        PersonImpl(const PersonImpl& other);
        void SetFirstName(const char* first_name);
        const char* GetFirstName() const;
        void SetSecondName(const char* second_name);
        const char* GetSecondName() const;
        void SetAge(unsigned int age);
        unsigned int GetAge() const;
        void SetMale(bool is_male);
        bool IsMale() const;
        void Dump(Example::IPrinter* printer) const;
        void Print(Example::IPrinter* printer, const char* text) const;
    };
}

#endif /* BEAUTIFUL_CAPI_PERSON_H */
