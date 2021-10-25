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
#include "DefaultPrinterImpl.h"

// By default newly created objects implies to have value 1 of reference counter
Example::PrinterBaseImpl::PrinterBaseImpl() : mRefCount(1)
{
    std::cout << "PrinterBase ctor" << std::endl;
}

// By default newly created objects implies to have value 1 of reference counter
Example::PrinterBaseImpl::PrinterBaseImpl(const PrinterBaseImpl& other) : mRefCount(1)
{
    std::cout << "PrinterBase copy ctor! (should never be called)" << std::endl;
}

Example::PrinterBaseImpl::~PrinterBaseImpl()
{
    std::cout << "PrinterBase dtor" << std::endl;
}

void Example::PrinterBaseImpl::AddRef()
{
    ++mRefCount;
}

void Example::PrinterBaseImpl::Release()
{
    --mRefCount;
    if (mRefCount <= 0)
    {
        delete this;
    }
}

Example::DefaultPrinterImpl::DefaultPrinterImpl()
{
    std::cout << "DefaultPrinter ctor" << std::endl;
}

Example::DefaultPrinterImpl::DefaultPrinterImpl(const DefaultPrinterImpl& other) : mQuality(other.mQuality)
{
    std::cout << "DefaultPrinter copy ctor" << std::endl;
}

Example::DefaultPrinterImpl::~DefaultPrinterImpl()
{
    std::cout << "DefaultPrinter dtor" << std::endl;
}

void Example::DefaultPrinterImpl::Print(const char* text) const
{
    if (text)
    {
        std::cout << "DefaultPrinter: " << text << std::endl;
    }
    else
    {
        std::cout << "DefaultPrinter: NULL" << std::endl;
    }
}

void Example::DefaultPrinterImpl::SetPrintingQuality(Example::EQuality quality)
{
    mQuality = quality;
}

Example::EQuality Example::DefaultPrinterImpl::GetPrintingQuality() const
{
    return mQuality;
}

Example::EPrintingDevice Example::DefaultPrinterImpl::GetDeviceType() const
{
    return Example::printer;
}

