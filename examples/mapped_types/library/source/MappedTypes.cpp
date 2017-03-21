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

#include <iostream>
#include <string>
#include "MappedTypes.h"

namespace MappedTypes
{
    const std::string& PersonImpl::GetFirstName() const
    {
        return firstName;
    }
    void PersonImpl::SetFirstName(const std::string& name)
    {
        firstName = name;
    }

    const char* PersonImpl::GetSecondName() const
    {
        return secondName.c_str();
    }
    void PersonImpl::SetSecondName(const char* sname)
    {
        secondName = sname;
    }

    int PersonImpl::GetAge() const
    {
        return age;
    }
    void PersonImpl::SetAge(int age)
    {
        this->age = age;
    }

    bool PersonImpl::IsMan() const
    {
        return isMan;
    }
    void PersonImpl::SetSex(bool sex)
    {
        isMan = sex;
    }

    const std::string& DeviceImpl::GetName() const
    {
        return name;
    }
    void DeviceImpl::SetName(const std::string& name)
    {
        this->name = name;
    }

    bool DeviceImpl::IsBusy() const
    {
        return isBusy;
    }
    void DeviceImpl::SetBusy(bool Busy)
    {
        isBusy = Busy;
    }
}
