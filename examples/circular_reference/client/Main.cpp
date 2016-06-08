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

#include <iostream>
#include "Circular/ClassA.h"
#include "Circular/ClassB.h"

int main()
{
    Circular::ClassAPtr a_object;
    Circular::ClassBPtr b_object;
    Circular::ClassAPtr a_object1;
    Circular::ClassBPtr b_object1;
    a_object->SetB(b_object);
    b_object1->SetA(a_object1);
    //TODO:
    //a_object->GetB()->SetA(a_object1);
    return EXIT_SUCCESS;
}
