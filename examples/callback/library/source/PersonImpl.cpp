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

#include <sstream>
#include "PersonImpl.h"

Example::PersonImpl::PersonImpl()
{
}

Example::PersonImpl::PersonImpl(const PersonImpl& other_person)
    : first_name(other_person.first_name),
    second_name(other_person.second_name),
    age(other_person.age),
    male(other_person.male)
{
}

void Example::PersonImpl::SetFirstName(const char* first_name)
{
    this->first_name = first_name;
}

const char* Example::PersonImpl::GetFirstName() const
{
    return this->first_name.c_str();
}

void Example::PersonImpl::SetSecondName(const char* second_name)
{
    this->second_name = second_name;
}

const char* Example::PersonImpl::GetSecondName() const
{
    return this->second_name.c_str();
}

void Example::PersonImpl::SetAge(unsigned int age)
{
    this->age = age;
}

unsigned int Example::PersonImpl::GetAge() const
{
    return this->age;
}

void Example::PersonImpl::SetMale(bool is_male)
{
    this->male = is_male;
}

bool Example::PersonImpl::IsMale() const
{
    return this->male;
}

void Example::PersonImpl::Dump(Example::IPrinter* printer) const
{
    class print_helper : public std::stringstream
    {
        Example::IPrinter *mPrinter;
    public:
        print_helper(Example::IPrinter *printer) : mPrinter(printer) {}
        ~print_helper()
        {
            if (mPrinter)
            {
                mPrinter->Print(str().c_str());
            }
        }
    };

    print_helper printer_io(printer);
    printer_io << "First Name: " << this->first_name << " Second Name: " << this->second_name << " Age: " << this->age << " Sex: " << (this->male ? "M" : "F");
}

