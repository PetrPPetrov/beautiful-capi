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
#include "Circular/ClassA.h"
#include "Circular/ClassB.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Circular::ClassARawPtr a_object;
    Circular::ClassBRawPtr b_object;
    Circular::ClassARawPtr a_object1;
    Circular::ClassBRawPtr b_object1;

    a_object.SetB(b_object);
    b_object1.SetA(a_object1);

    Circular::ClassARawPtr tmp_object = b_object1.GetA();
    tmp_object.SetB(b_object);

    a_object.GetB()->SetA(a_object1); // We need to use "->" operator here, as GetB() returns forward_pointer_holder<Circular::ClassB>

    a_object.Delete();
    b_object.Delete();
    a_object1.Delete();
    b_object1.Delete();
    return EXIT_SUCCESS;
}
