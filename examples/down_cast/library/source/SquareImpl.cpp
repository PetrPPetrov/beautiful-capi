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
#include "SquareImpl.h"

Example::SquareImpl::SquareImpl() : m_size(1.0)
{
    std::cout << "Square ctor" << std::endl;
}

Example::SquareImpl::~SquareImpl()
{
    std::cout << "Square dtor" << std::endl;
}

void Example::SquareImpl::Show()
{
    std::cout << "SquareImpl::Show(), size = " << m_size << std::endl;
}

int Example::SquareImpl::GetPointsCount() const
{
    return 4;
}

void Example::SquareImpl::SetSize(double size)
{
    m_size = size;
}
