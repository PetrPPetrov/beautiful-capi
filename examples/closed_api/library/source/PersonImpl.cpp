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
    std::cout << "Person ctor" << std::endl;
}

Example::PersonImpl::PersonImpl(const PersonImpl& other_person)
    : first_name(other_person.first_name),
    last_name(other_person.last_name),
    age(other_person.age),
    sex(other_person.sex)
{
    std::cout << "Person copy ctor" << std::endl;
}

Example::PersonImpl::~PersonImpl()
{
    std::cout << "Person dtor" << std::endl;
}

void Example::PersonImpl::SetFirstName(const char* first_name)
{
    this->first_name = first_name;
}

const char* Example::PersonImpl::GetFirstName() const
{
    return this->first_name.c_str();
}

void Example::PersonImpl::SetLastName(const char* last_name)
{
    this->last_name = last_name;
}

const char* Example::PersonImpl::GetLastName() const
{
    return this->last_name.c_str();
}

void Example::PersonImpl::SetAge(unsigned int age)
{
    this->age = age;
}

unsigned int Example::PersonImpl::GetAge() const
{
    return this->age;
}

void Example::PersonImpl::SetSex(Example::ESex sex)
{
    this->sex = sex;
}

Example::ESex Example::PersonImpl::GetSex() const
{
    return sex;
}
