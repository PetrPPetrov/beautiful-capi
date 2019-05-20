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

#ifndef BEAUTIFUL_CAPI_MIXED_SEMANTIC_PRINTER_H
#define BEAUTIFUL_CAPI_MIXED_SEMANTIC_PRINTER_H

#include <iostream>
#include <string>
#include <vector>
#include <stddef.h>
#include "NameImpl.h"
#include "PersonImpl.h"
#include "AddressImpl.h"

namespace MixedSemantic
{
    class PrinterImpl
    {
    public:
        void Show(MixedSemantic::NameImpl name)
        {
            std::cout << "Fist Name: " << name.GetFirstName() << std::endl;
        }

         void ShowByPointer(const MixedSemantic::NameImpl* name)
        {
            std::cout << "Father Name: " << name->GetFatherName() << std::endl;
        }

        void ShowByReference(const MixedSemantic::NameImpl& name)
        {
            std::cout << "Last Name: " << name.GetLastName() << std::endl;
        }

        void Show(MixedSemantic::PersonImpl person)
        {
            std::cout << "Person birth day: " << person.GetDay() << std::endl;
        }

        void ShowByReference(const MixedSemantic::PersonImpl& person)
        {
            std::cout << "Person birth month: " << person.GetMonth() << std::endl;
        }

        void ShowByPointer(MixedSemantic::PersonImpl* person)
        {
            std::cout << "Person birth year: " << person->GetYear() << std::endl;
        }

        void Show(MixedSemantic::AddressImpl addr)
        {
            std::cout << "Person street: " << addr.GetStreetName() << std::endl;
        }

        void ShowByPointer(MixedSemantic::AddressImpl* addr)
        {
            std::cout << "Person city: " << addr->GetCity() << std::endl;
        }

        void ShowByReference(const MixedSemantic::AddressImpl& addr)
        {
            std::cout << "Person state: " << addr.GetState() << std::endl;
        }
    };
}

#endif /* BEAUTIFUL_CAPI_MIXED_SEMANTIC_PRINTER_H */
