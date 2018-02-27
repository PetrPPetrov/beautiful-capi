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
#include "DoxygenDoc.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif

    DoxygenDoc::Printer printer;

    DoxygenDoc::Name name("Jon", "Snow");
    printer.Show(name);
    printer.ShowByPointer(name);
    printer.ShowByReference(name);

    DoxygenDoc::PersonRawPtr person;
    person->SetName(name);
    person->SetDay(27);
    person->SetMonth(12);
    person->SetYear(324);
    printer.Show(person);
    printer.ShowByPointer(person);
    printer.ShowByReference(person);

    DoxygenDoc::AddressPtr address;
    address->SetStreetName("Wall");    
    person->SetAddress(address);
    printer.Show(person->GetAddress());
    printer.ShowByPointer(person->GetAddress());
    printer.ShowByReference(person->GetAddress());

    person->Delete();
    return EXIT_SUCCESS;
}
