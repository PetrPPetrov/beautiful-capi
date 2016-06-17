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
#include "TriangleImpl.h"

Example::TriangleImpl::TriangleImpl() 
    : m_x1(0.0), m_y1(0.0), m_x2(1.0), m_y2(0.0), m_x3(0.0), m_y3(1.0)
{
    std::cout << "Triangle ctor" << std::endl;
}

Example::TriangleImpl::~TriangleImpl()
{
    std::cout << "Triangle dtor" << std::endl;
}

void Example::TriangleImpl::Show()
{
    std::cout << "TriangleImpl::Show(), x1 = " << m_x1 << " y1 = " << m_y1
              << " x2 = " << m_x2 << " y2 = " << m_y2
              << " x3 = " << m_x3 << " y3 = " << m_y3 << std::endl;
}

int Example::TriangleImpl::GetPointsCount() const
{
    return 3;
}

void Example::TriangleImpl::SetPoints(double x1, double y1, double x2, double y2, double x3, double y3)
{
    m_x1 = x1;
    m_y1 = y1;
    m_x2 = x2;
    m_y2 = y2;
    m_x3 = x3;
    m_y3 = y3;
}
