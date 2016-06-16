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
#include "plotter_impl.h"

// By default newly created objects implies to have value 1 of reference counter
hello_world::plotter_impl::plotter_impl() : reference_count(1)
{
    std::cout << "Plotter ctor" << std::endl;
}

hello_world::plotter_impl::~plotter_impl()
{
    std::cout << "Plotter dtor" << std::endl;
}

void hello_world::plotter_impl::add_ref()
{
    if (this)
    {
        ++reference_count;
    }
}

void hello_world::plotter_impl::release()
{
    if (this)
    {
        --reference_count;
        if (reference_count <= 0)
        {
            delete this;
        }
    }
}

void hello_world::plotter_impl::draw() const
{
    std::cout << "plotter::draw()" << std::endl;
}
