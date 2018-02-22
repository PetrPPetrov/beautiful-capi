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
#include "Template.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Example::VectorOf<int> vector;
    vector.PushBack(5);
    vector.PushBack(7);
    vector.PushBack(3);
    vector.PushBack(10);
    vector.dump();

    Example::VectorOf<double> vector2;
    vector2.PushBack(3.14);
    vector2.PushBack(2.71);
    vector2.dump();

    Example::Position<float> position;
    position.SetY(15.5);
    position.dump();

    Example::Position4D<double> position2;
    position2.SetW(0.5);
    position2.dump();

    Example::VectorOf<Example::Position4D<float> > vector3;
    vector3.PushBack(Example::Position4D<float>());
    vector3.PushBack(Example::Position4D<float>());
    vector3.dump();

    Example::VectorOf<Example::VectorOf<Example::Position4D<float> > > vectorz;
    vectorz.PushBack(vector3);
    vectorz.PushBack(vector3);
    vectorz.dump();

    Example::VectorOfObjectsDerivedPtr<Example::ModelPtr<double> > model_vector;
    Example::ModelPtr<double> model1;
    Example::ModelPtr<double> model2;
    model1->SetName("model1");
    model2->SetName("model2");

    model_vector->PushBack(model1);
    model_vector->PushBack(model2);
    model_vector.dump();

    std::cout << model_vector.GetA() << std::endl;

    Example::VectorOf<char> dummy;
    dummy.dump();

    return EXIT_SUCCESS;
}
