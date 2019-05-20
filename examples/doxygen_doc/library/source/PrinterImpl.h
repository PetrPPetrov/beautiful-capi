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

#ifndef BEAUTIFUL_CAPI_DOXYGEN_DOC_PRINTER_H
#define BEAUTIFUL_CAPI_DOXYGEN_DOC_PRINTER_H

#include <iostream>
#include <string>
#include <vector>
#include <stddef.h>
#include "NameImpl.h"
#include "AddressImpl.h"
#include "PersonImpl.h"

namespace DoxygenDoc
{
    class PrinterImpl
    {
    public:
        void Show(DoxygenDoc::NameImpl name)
        {
            std::cout << "First Name: " << name.GetFirstName() << std::endl;
        }

         void ShowByPointer(const DoxygenDoc::NameImpl* name)
        {
            std::cout << "First Name: " << name->GetFirstName() << std::endl;
        }

        void ShowByReference(const DoxygenDoc::NameImpl& name)
        {
            std::cout << "Last Name: " << name.GetLastName() << std::endl;
        }

        void Show(DoxygenDoc::PersonImpl person)
        {
            std::cout << "Person birth day: " << person.GetDay() << std::endl;
        }

        void ShowByReference(const DoxygenDoc::PersonImpl& person)
        {
            std::cout << "Person birth month: " << person.GetMonth() << std::endl;
        }

        void ShowByPointer(DoxygenDoc::PersonImpl* person)
        {
            std::cout << "Person birth year: " << person->GetYear() << std::endl;
        }

        void Show(DoxygenDoc::AddressImpl addr)
        {
            std::cout << "Person street: " << addr.GetStreetName() << std::endl;
        }

        void ShowByPointer(DoxygenDoc::AddressImpl* addr)
        {
            std::cout << "Person city: " << addr->GetCity() << std::endl;
        }

        void ShowByReference(const DoxygenDoc::AddressImpl& addr)
        {
            std::cout << "Person state: " << addr.GetState() << std::endl;
        }
    };
}

#endif /* BEAUTIFUL_CAPI_DOXYGEN_DOC_PRINTER_H */
