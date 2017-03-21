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
#include "MappedTypes.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif   
    MappedTypes::Person person;
    person.SetFirstName("John");
    person.SetSecondName("Snow");
    person.SetAge(14);
    person.SetSex(true);
    std::cout << person.GetFirstName() << std::endl;
    std::cout << person.GetSecondName() << std::endl;
    std::cout << person.GetAge() << std::endl;
    std::cout << person.IsMan() << std::endl;
        
    MappedTypes::Device device;
    device.SetName("Printer");
    device.SetBusy(false);
    std::cout << device.GetName() << std::endl;  
    std::cout << device.IsBusy() << std::endl;    
    return EXIT_SUCCESS;
}
