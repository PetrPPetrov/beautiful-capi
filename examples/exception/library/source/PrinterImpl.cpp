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
#include "PrinterImpl.h"
#include "Exception/NullArgumentImpl.h"

Example::PrinterImpl::PrinterImpl()
{
    std::cout << "Printer ctor" << std::endl;
}

Example::PrinterImpl::PrinterImpl(const Example::PrinterImpl& other)
    : mPreviousText(other.mPreviousText)
{
    std::cout << "Printer copy ctor" << std::endl;
}

Example::PrinterImpl::~PrinterImpl()
{
    std::cout << "Printer dtor" << std::endl;
}

const char* Example::PrinterImpl::Show(const char* text)
{
    if (!text)
    {
        throw Exception::NullArgumentImpl("text");
    }
    std::cout << "print text: " << text << std::endl;
    mPreviousText = std::string(text);
    return mPreviousText.c_str();
}

void Example::PrinterImpl::PowerOn()
{
    std::cout << "Printer power on" << std::endl;
}

void Example::PrinterImpl::PowerOff()
{
    std::cout << "Printer power off" << std::endl;
}

