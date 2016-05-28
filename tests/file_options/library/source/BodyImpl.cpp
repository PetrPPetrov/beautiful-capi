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
#include "BodyImpl.h"

Example::Geometry::Brep::BodyImpl::BodyImpl()
{
    std::cout << "Body ctor" << std::endl;
}

Example::Geometry::Brep::BodyImpl::BodyImpl(const Example::Geometry::Brep::BodyImpl& other)
    : mName(other.mName)
{
    std::cout << "Body copy ctor" << std::endl;
}

Example::Geometry::Brep::BodyImpl::~BodyImpl()
{
    std::cout << "Body dtor" << std::endl;
}

const char* Example::Geometry::Brep::BodyImpl::GetName() const
{
    return mName.c_str();
}

void Example::Geometry::Brep::BodyImpl::SetName(const char* value)
{
    mName = value;
}
