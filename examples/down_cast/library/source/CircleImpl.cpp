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
#include "CircleImpl.h"

Example::CircleImpl::CircleImpl() : m_radius(10.0)
{
    std::cout << "Circle ctor" << std::endl;
}

Example::CircleImpl::CircleImpl(const CircleImpl& other) : m_radius(other.m_radius)
{
    std::cout << "Circle copy ctor" << std::endl;
}

Example::CircleImpl::~CircleImpl()
{
    std::cout << "Circle dtor" << std::endl;
}

void Example::CircleImpl::Show() const
{
    std::cout << "CircleImpl::Show(), radius = " << m_radius << std::endl;
}

void Example::CircleImpl::SetRadius(double radius)
{
    m_radius = radius;
}
