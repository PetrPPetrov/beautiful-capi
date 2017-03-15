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
#include "OverloadSuffix.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    std::cout << "Namespace overload_suffix_mode = Notify" << std::endl;
    std::cout << "Class overload_suffix_mode = Silent" << std::endl;
    std::cout << "Create Printer" << std::endl;    
    OverloadSuffix::Printer printer;
    const OverloadSuffix::Printer& printer2 = printer;
    
    std::cout << "Overloaded methods:" << std::endl;
    printer.Show();
    printer2.Show();
    printer.Show(7);
    printer.Show(4.2);
        
    std::cout << "Overloaded functions:" << std::endl;
    OverloadSuffix::Show();
    OverloadSuffix::Show(5);
    OverloadSuffix::Show(1.3);
        
    return EXIT_SUCCESS;
}
