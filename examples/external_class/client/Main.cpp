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
#include "PrinterNS.h"
#include "Components.h"
#include "CompC.h"
#include "Classes.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif

    PrinterNS::Printer printer;
    Classes::ClassA a;
    Classes::ClassBRawPtr b;
    Classes::ClassCPtr c;
    a.SetValue(3);
    b->SetValue("str");
    c->SetValue(7.2);
    Components::ComponentA comp_a;
    comp_a.SetA(a);
    comp_a.SetB(b);
    comp_a.SetC(c);
    Components::ComponentBRawPtr comp_b;
    comp_b->SetA(a);
    comp_b->SetB(b);
    comp_b->SetC(c);
    CompC::ComponentCPtr comp_c;
    comp_c->SetA(a);
    comp_c->SetB(b);
    comp_c->SetC(c);

    printer.Show(comp_a);
    printer.Show(comp_b);
    printer.Show(comp_c);

    std::cout << "Change values to '8', 'another string' and '3.14':" << std::endl;
    a.SetValue(8);
    b->SetValue("another string");
    c->SetValue(3.14);

    printer.Show(comp_a);
    printer.Show(comp_b);    
    printer.Show(comp_c);    
    return EXIT_SUCCESS;
}
