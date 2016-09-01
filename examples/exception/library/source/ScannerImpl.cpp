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
#include "ScannerImpl.h"

// By default newly created objects implies to have value 1 of reference counter
Example::ScannerImpl::ScannerImpl() : mRefCount(1)
{
    std::cout << "Scanner ctor" << std::endl;
}

// By default newly created objects implies to have value 1 of reference counter
Example::ScannerImpl::ScannerImpl(const ScannerImpl& other) : mRefCount(1), mScannedText(other.mScannedText)
{
    std::cout << "Scanner copy ctor! (should be never called)" << std::endl;
}

Example::ScannerImpl::~ScannerImpl()
{
    std::cout << "Scanner dtor" << std::endl;
}

void Example::ScannerImpl::AddRef()
{
    if (this)
    {
        ++mRefCount;
    }
}

void Example::ScannerImpl::Release()
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

const char* Example::ScannerImpl::ScanText()
{
    mScannedText = "Hello World!";
    return mScannedText.c_str();
}

void Example::ScannerImpl::PowerOn()
{
    std::cout << "Scanner power on" << std::endl;
}

void Example::ScannerImpl::PowerOff()
{
    std::cout << "Scanner power off" << std::endl;
}
