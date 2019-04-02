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
#include <cctype>
#include <iostream>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <stdint.h>
//#include "ExampleKeys.h"
#include "Example.h"


void dump(const Example::Person& person)
{
    std::cout << "==========" << std::endl;
    std::cout << "Name: " << person.GetFirstName() << " " << person.GetLastName() << std::endl;
    std::cout << "Age: " << person.GetAge() << std::endl;
    std::cout << "Sex: " << (person.GetSex() == Example::Person::male ? "Male" : "Female") << std::endl;
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Example::Person famous_person;
    famous_person.SetFirstName("Isaac");
    famous_person.SetLastName("Newton");
    famous_person.SetAge(26);
    famous_person.SetSex(Example::Person::male);

    dump(famous_person);

    Example::Education::School::Teacher teacher;
    teacher.SetFirstName("John");
    teacher.SetAge(25);
    teacher.SetSex(Example::Person::male);
    teacher.Teach();

    Example::Education::A::University::Professor professor;
    professor.SetFirstName("Vanessa");
    professor.SetSex(Example::Person::female);
    professor.Do();

    return EXIT_SUCCESS;
}
