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
#include "MixedSemantic2.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    std::cout << "Create address_ref." << std::endl; 
    MixedSemantic2::AddressPtr address_ref;
    std::cout << "Create address_raw and address_copy appropriating them address_ref." << std::endl << std::endl; 
    MixedSemantic2::AddressRawPtr address_raw = address_ref;
    MixedSemantic2::AddressCopy address_copy = address_ref;
    
    std::cout << "Set address_ref name: Avenu N.5"  << std::endl;
    address_ref->SetStreetName("Avenu N.5");
    
    std::cout << "Names:"  << std::endl;
    std::cout << "street name (RefCount) = " << address_ref->GetStreetName() << std::endl;
    std::cout << "street name (RawPtr) = " << address_raw->GetStreetName() << std::endl;
    std::cout << "street name (Copy) = " << address_copy.GetStreetName() << std::endl << std::endl; 
    
    std::cout << "Set address_raw name: Koshevogo"  << std::endl;
    address_raw->SetStreetName("Koshevogo");
    
    std::cout << "Names:"  << std::endl;
    std::cout << "street name (RefCount) = " << address_ref->GetStreetName() << std::endl;
    std::cout << "street name (RawPtr) = " << address_raw->GetStreetName() << std::endl;
    std::cout << "street name (Copy) = " << address_copy.GetStreetName() << std::endl << std::endl;   
    
    std::cout << "Set address_copy name: Lenina" << std::endl;
    address_copy.SetStreetName("Lenina");
    
    std::cout << "Names:"  << std::endl;
    std::cout << "street name (RefCount) = " << address_ref->GetStreetName() << std::endl;
    std::cout << "street name (RawPtr) = " << address_raw->GetStreetName() << std::endl;
    std::cout << "street name (Copy) = " << address_copy.GetStreetName() << std::endl << std::endl;  
        
    
    MixedSemantic2::Printer printer;
    std::cout << "Create copy semantic name." << std::endl << std::endl; 
    MixedSemantic2::Name name("default_name", "", "");
    std::cout << "name:" << std::endl;
    printer.Show(name);
    
    std::cout << "Create RawPtr semantic name_ptr, appropriating him name." << std::endl; 
    MixedSemantic2::NameRawPtr name_ptr = name; 
    std::cout << "change name_ptr"  << std::endl; 
    name_ptr.SetFirstName("changed_name"); 
    std::cout << "name_ptr:" << std::endl;
    printer.Show(name); 
    std::cout << std::endl;

    
    std::cout << "Create RawPtr semantic Person:" << std::endl; 
    MixedSemantic2::PersonRawPtr person;
    person.SetName(name);
    person.GetName().SetFirstName("inplace modification");
    std::cout << person.GetName().GetFirstName() << std::endl; 
    person.SetDay(27);
    person.SetMonth(12);
    person.SetYear(324);
    printer.Show(person);
    printer.ShowByPointer(person);
    printer.ShowByReference(person);
    std::cout << std::endl;
    
    std::cout << "Create copy semantic Person and appropriating him Person." << std::endl; 
    MixedSemantic2::PersonCopy person_copy = person;
    std::cout << "Change person_copy" << std::endl; 
    person_copy.SetDay(0);
    person_copy.SetMonth(0);
    person_copy.SetYear(0);  
    printer.Show(person_copy);    
    printer.ShowByPointer(person_copy);
    printer.ShowByReference(person_copy);
    std::cout << std::endl;
    
    std::cout << "original Person:" << std::endl; 
    printer.Show(person);    
    printer.ShowByPointer(person);
    printer.ShowByReference(person);

    return EXIT_SUCCESS;
}
