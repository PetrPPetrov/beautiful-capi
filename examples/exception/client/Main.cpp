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
#include <stdint.h>
#include "Example.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    try
    {
        Example::Printer printer;
        Example::ScannerPtr scanner;

        scanner->PowerOn();
        std::cout << "Scanned text: " << scanner->ScanText() << std::endl;
        scanner->PowerOff();

        printer.PowerOn();
        printer.Show("from main()");
        std::cout << "Trying to show null pointer" << std::endl;
        printer.Show(0);
        printer.PowerOff();
    }
    catch (Exception::NullArgument& null_argument_exception)
    {
        std::cout << "    *** Exception::NullArgument was thrown" << std::endl;
        std::cout << "    " << null_argument_exception.GetErrorText() << std::endl;
        std::cout << "    argument: " << null_argument_exception.GetArgumentName() << std::endl;
    }
    catch (Exception::BadArgument& null_argument_exception)
    {
        std::cout << "    *** Exception::BadArgument was thrown" << std::endl;
        std::cout << "    " << null_argument_exception.GetErrorText() << std::endl;
    }
    catch (Exception::Generic& generic_exception)
    {
        std::cout << "    *** Exception::Generic was thrown" << std::endl;
        std::cout << "    " << generic_exception.GetErrorText() << std::endl;
    }
    catch (const std::exception& exception)
    {
        std::cout << "    *** std::exception was thrown" << std::endl;
        std::cout << "    " << exception.what() << std::endl;
    }
    catch (...)
    {
        std::cout << "    *** Unknown exception was hrown" << std::endl;
    }

    return EXIT_SUCCESS;
}
