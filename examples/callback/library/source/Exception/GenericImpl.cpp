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
#include "Exception/GenericImpl.h"

Exception::GenericImpl::GenericImpl()
    : mMessage("generic")
{
    std::cout << "Generic ctor" << std::endl;
}

Exception::GenericImpl::GenericImpl(const std::string& message)
    : mMessage(message)
{
    std::cout << "Generic ctor" << std::endl;
}

Exception::GenericImpl::GenericImpl(const GenericImpl& other)
    : mMessage(other.mMessage)
{
    std::cout << "Generic copy ctor" << std::endl;
}

Exception::GenericImpl::~GenericImpl()
{
    std::cout << "Generic dtor" << std::endl;
}

const char* Exception::GenericImpl::GetErrorText() const
{
    return mMessage.c_str();
}
