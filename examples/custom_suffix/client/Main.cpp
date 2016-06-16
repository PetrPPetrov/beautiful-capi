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
#include <cstdlib>
#include "hello_world/hello_world.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    hello_world::printer printer; // It has copy semantic (value semantic)
    printer.show();

    hello_world::scanner_raw_ptr scanner; // It has non-owning pointer (raw pointer) semantic
    if (!scanner)
    {
        std::cout << "Error, scanner is null!" << std::endl;
        return EXIT_FAILURE;
    }
    scanner->scan();
    scanner->deallocate(); // We need to manually deallocate object from non-owning pointer

    hello_world::plotter_ptr plotter; // It has reference counted smart pointer semantic
    if (plotter->is_null())
    {
        std::cout << "Error, plotter is null!" << std::endl;
        return EXIT_FAILURE;
    }
    if (plotter->is_not_null())
    {
        plotter->draw();
    }

    return EXIT_SUCCESS;
}
