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
#include "SphereImpl.h"

Example::Geometry::SphereImpl::SphereImpl()
{
    std::cout << "Sphere ctor" << std::endl;
}

Example::Geometry::SphereImpl::SphereImpl(const Example::Geometry::SphereImpl& other)
    : mRadius(other.mRadius)
{
    std::cout << "Sphere copy ctor" << std::endl;
}

Example::Geometry::SphereImpl::~SphereImpl()
{
    std::cout << "Sphere dtor" << std::endl;
}

double Example::Geometry::SphereImpl::GetRadius() const
{
    return mRadius;
}

void Example::Geometry::SphereImpl::SetRadius(double value)
{
    mRadius = value;
}
