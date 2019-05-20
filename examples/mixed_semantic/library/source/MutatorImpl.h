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

#ifndef BEAUTIFUL_CAPI_MIXED_SEMANTIC_MUTATOR_H
#define BEAUTIFUL_CAPI_MIXED_SEMANTIC_MUTATOR_H

#include <iostream>
#include <string>
#include <vector>
#include <stddef.h>
#include "AddressImpl.h"
#include "NameImpl.h"
#include "PersonImpl.h"

namespace MixedSemantic
{
    class MutatorImpl
    {
    public:
        void Mutate(MixedSemantic::NameImpl name)
        {
            std::string new_name = name.GetFirstName();
            new_name += "_mutated";
            name.SetFirstName(new_name.c_str());
        }

         void MutateByPointer(MixedSemantic::NameImpl* name)
        {
            std::string new_name = name->GetFatherName();
            new_name += "_mutated";
            name->SetFatherName(new_name.c_str());
        }

        void MutateByReference(MixedSemantic::NameImpl& name)
        {
            std::string new_name = name.GetLastName(); 
            new_name += "_mutated";            
            name.SetLastName(new_name.c_str());
            //std::cout << new_name <<std::endl;
        }

        void Mutate(MixedSemantic::PersonImpl person)
        {
            person.SetDay(person.GetDay() + 1);
        }

        void MutateByReference(MixedSemantic::PersonImpl& person)
        {
            person.SetMonth(person.GetMonth() + 1);
        }

        void MutateByPointer(MixedSemantic::PersonImpl* person)
        {
            person->SetYear(person->GetYear() + 1);
        }

        void Mutate(MixedSemantic::AddressImpl address)
        {
            std::string new_address = address.GetStreetName();
            new_address += "_mutated";
            address.SetStreetName(new_address.c_str());
        }

        void MutateByPointer(MixedSemantic::AddressImpl* address)
        {
            std::string new_address = address->GetCity();
            new_address += "_mutated";
            address->SetCity(new_address.c_str());
        }

        void MutateByReference(MixedSemantic::AddressImpl& address)
        {
            address.SetState(address.GetState() + 1);
        }
    };
}

#endif /* BEAUTIFUL_CAPI_MIXED_SEMANTIC_MUTATOR_H */
