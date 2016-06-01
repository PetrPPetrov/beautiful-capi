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
#include "PageImpl.h"

// Newly created objects implies to have value 1 of reference counter
Example::PageImpl::PageImpl() : mRefCount(1), mWidth(200), mHeight(100)
{
    std::cout << "Page ctor" << std::endl;
}

Example::PageImpl::~PageImpl()
{
    std::cout << "Page dtor" << std::endl;
}

void Example::PageImpl::AddRef()
{
    if (this)
    {
        ++mRefCount;
    }
}

void Example::PageImpl::Release()
{
    if (this)
    {
        --mRefCount;
        if (mRefCount <= 0)
        {
            delete this;

        }
    }
}

size_t Example::PageImpl::GetWidth() const
{
    return mWidth;
}

size_t Example::PageImpl::GetHeight() const
{
    return mHeight;
}

void Example::PageImpl::SetWidth(size_t value)
{
    mWidth = value;
}

void Example::PageImpl::SetHeight(size_t value)
{
    mHeight = value;
}
