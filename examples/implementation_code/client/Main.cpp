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
#include <stdint.h>
#include "STL.h"

template<typename T>
void dump(const STL::Vector<T>& vector)
{
    std::cout << "Vector has " << vector.GetSize() << " elements" << std::endl;
    for (size_t i = 0; i < vector.GetSize(); ++i)
    {
        std::cout << vector.GetElement(i) << " ";
    }
    std::cout << std::endl;
}

void dump(const STL::Person& person)
{
    std::cout << "==========" << std::endl;
    std::cout << "Name: " << person.GetFirstName().CStr() << std::endl;
    std::cout << "Surname: " << person.GetSecondName().CStr() << std::endl;
    std::cout << "Age: " << person.GetAge() << std::endl;
}

void dump(STL::Community& community)
{
    std::cout << "====================" << std::endl;
    std::cout << "Title: " << community.GetTitle().CStr() << std::endl;
    std::cout << "this community has " << community.Members()->GetSize() << " members." << std::endl;
    for (size_t i = 0; i < community.Members()->GetSize(); ++i)
    {
        dump(community.Members()->GetElement(i));
    }
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    STL::Vector<double> numbers;
    numbers.PushBack(3.14);
    numbers.PushBack(2.72);

    dump(numbers);

    numbers.SetElement(0, 333);
    dump(numbers);

    std::cout << "sin(90 degrees) = " << STL::SinDegree(90) << std::endl;

    try
    {
        throw STL::Exception(STL::String("range error exception"));
    }
    catch (const STL::Exception& exception)
    {
        std::cout << "Expected exception was caught, error text: " << exception.What() << std::endl;
    }

    STL::Person man;
    man.SetAge(32);
    man.SetFirstName(STL::String("John"));
    man.SetSecondName(STL::String("Watson"));
    dump(man);

    STL::Community soccer_community;
    soccer_community.SetTitle("Soccer Community");
    soccer_community.Members()->PushBack(man);
    soccer_community.Members()->PushBack(man);
    soccer_community.Members()->Element(1)->SetFirstName(STL::String("Bill"));
    soccer_community.Members()->Element(1)->SetSecondName(STL::String("Johnson"));
    soccer_community.Members()->Element(1)->SetAge(29);
    dump(soccer_community);

    return EXIT_SUCCESS;
}
