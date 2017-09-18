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

#if defined(_WIN32) && defined(_DEBUG)
#include <crtdbg.h>
#endif
#include <iostream>
#include <stdint.h>
#include "Example.h"

void f1(Example::PrinterPtr p)
{
    p->Show("from f1()");
}

Example::PrinterPtr create_printer()
{
    Example::PrinterPtr new_printer;
    new_printer->Show("from create_printer()");
    return new_printer;
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Example::PrinterPtr printer = create_printer();
    printer->Show("from main()");
    f1(printer);

    Example::Dumper dumper;
    dumper.SetPrinter(printer);
    dumper.Dump();

    Example::PrinterPtr printer2 = dumper.GetPrinter();
    printer2->Show("printer2");

    return EXIT_SUCCESS;
}
