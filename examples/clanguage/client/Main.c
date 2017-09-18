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
#include <stdlib.h>
#include <stdint.h>
#include "ExampleCapi.h"

void f1(void* p)
{
    example_printer_show(p, "from f1()");
    example_printer_delete(p);
}

void* create_printer()
{
    void* new_printer = example_printer_new();
    example_printer_show(new_printer, "from create_printer()");
    return new_printer;
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif

    void* printer = create_printer();
    example_printer_show(printer, "from main()");
    void* printer_copy = example_printer_copy(printer);
    f1(printer_copy);

    void* dumper_t = example_dumper_new();
    example_dumper_set_printer(dumper_t, printer);
    example_dumper_dump(dumper_t);

    void* printer2 = example_dumper_get_printer_const(dumper_t);
    example_printer_show(printer2, "printer2");

    example_printer_delete(printer);
    example_dumper_delete(dumper_t);
    example_printer_delete(printer2);

    return EXIT_SUCCESS;
}
