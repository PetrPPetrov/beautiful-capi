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
#include <cstdlib>
#include "Example.h"

void f1(Example::Printer p)
{
    p.Show("from f1()");
}

Example::Printer create_printer()
{
    Example::Printer new_printer;
    new_printer.Show("from create_printer()");
    return new_printer;
}

int main()
{
    Example::Printer printer = create_printer();
    printer.Show("from main()");
    f1(printer);

    return EXIT_SUCCESS;
}
