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

namespace OverloadSuffix
{
    void PrinterImpl::Show()
    {
        std::cout << "\tMethod without parameters" << std::endl;
    }
    void PrinterImpl::Show() const
    {
        std::cout << "\tConst method without parameters" << std::endl;
    }    
    void PrinterImpl::Show(int a)
    {
        std::cout << "\tOverloaded method with manually installed suffix \"Int\". Int value = " << a << std::endl;
    }
    void PrinterImpl::Show(double a)
    {
        std::cout << "\tOverloaded method with automatic installed suffix \"1\". Double value = " << a << std::endl;
    }

    void Show()
    {
        std::cout << "\tFunction without parameters" << std::endl;
    }
    void Show(int a)
    {
        std::cout << "\tOverloaded function with manually installed suffix \"Int\". Int value = " << a << std::endl;
    }
    void Show(double a)
    {
        std::cout << "\tOverloaded function with automatic installed suffix \"1\". Double value = " << a << std::endl;
    }
}

