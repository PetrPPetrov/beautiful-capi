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
#include "DumperImpl.h"

Example::DumperImpl::DumperImpl()
{
    std::cout << "Dumper ctor" << std::endl;
}

Example::DumperImpl::DumperImpl(const Example::DumperImpl& other)
{
    std::cout << "Dumper copy ctor" << std::endl;
}

Example::DumperImpl::~DumperImpl()
{
    std::cout << "Dumper dtor" << std::endl;
}

Example::PrinterImpl* Example::DumperImpl::GetPrinter() const
{
    return mPrinter;
}

void Example::DumperImpl::SetPrinter(Example::PrinterImpl* printer)
{
    mPrinter = printer;
}

void Example::DumperImpl::Dump() const
{
    mPrinter->Show("Dumper::Dump(): dump some text here");
}
