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
#include "ClassAImpl.h"
#include "ClassBImpl.h"

Circular::ClassAImpl::ClassAImpl() : mBInstance(0)
{
    std::cout << "ClassA ctor" << std::endl;
}

Circular::ClassAImpl::ClassAImpl(const ClassAImpl& other) : mBInstance(other.mBInstance)
{
    std::cout << "ClassA copy ctor" << std::endl;
}

Circular::ClassAImpl::~ClassAImpl()
{
    std::cout << "ClassA dtor" << std::endl;
}

void Circular::ClassAImpl::SetB(ClassBImpl* class_b)
{
    mBInstance = class_b;
}

Circular::ClassBImpl* Circular::ClassAImpl::GetB() const
{
    return mBInstance;
}
