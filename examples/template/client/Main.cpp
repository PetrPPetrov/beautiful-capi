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
#include "Template.h"

template<typename SimpleType>
void dump(SimpleType value)
{
    std::cout << value << " ";
}

template<typename T>
void dump(const Example::Position<T>& position)
{
    std::cout << "X: ";
    dump(position.GetX());
    std::cout << "Y: ";
    dump(position.GetY());
    std::cout << "Z: ";
    dump(position.GetZ());
    std::cout << std::endl;
}

template<typename T>
void dump(const Example::Position4D<T>& position)
{
    dump(static_cast<const Example::Position<T>&>(position));
    std::cout << "W: ";
    dump(position.GetW());
    std::cout << std::endl;
}

template<typename T>
void dump(const Example::VectorOf<T>& vector)
{
    std::cout << "Vector has " << vector.GetSize() << " elements" << std::endl;
    for (int i = 0; i < vector.GetSize(); ++i)
    {
        dump(static_cast<T>(vector.GetItem(i)));
    }
    std::cout << std::endl;
}

template<typename T>
void dump(Example::ModelPtr<T> model)
{
    std::cout << "Model" << std::endl;
    std::cout << "name: " << model.GetName() << std::endl;
    dump(static_cast<Example::Position<T> >(model.GetPosition()));
}

template<typename T>
void dump(const Example::VectorOfObjectsPtr<T>& vector)
{
    std::cout << "Vector has " << vector.GetSize() << " elements" << std::endl;
    for (int i = 0; i < vector.GetSize(); ++i)
    {
        dump(static_cast<T>(vector.GetItem(i)));
    }
    std::cout << std::endl;
}

template<typename T>
void dump(const Example::VectorOfObjectsDerivedPtr<T>& vector)
{
    std::cout << "VectorOfObjectsDerivedPtr" << std::endl;
    dump(static_cast<const Example::VectorOfObjectsPtr<T>&>(vector));
}

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
    dump(vector);

    Example::VectorOf<double> vector2;
    vector2.PushBack(3.14);
    vector2.PushBack(2.71);
    dump(vector2);

    Example::Position<float> position;
    position.SetY(15.5);
    dump(position);

    Example::Position4D<double> position2;
    position2.SetW(0.5);
    dump(position2);

    Example::VectorOf<Example::Position4D<float> > vector3;
    vector3.PushBack(Example::Position4D<float>());
    vector3.PushBack(Example::Position4D<float>());
    dump(vector3);

    Example::VectorOf<Example::VectorOf<Example::Position4D<float> > > vectorz;
    vectorz.PushBack(vector3);
    vectorz.PushBack(vector3);
    dump(vectorz);

    Example::VectorOfObjectsDerivedPtr<Example::ModelPtr<double> > model_vector;
    Example::ModelPtr<double> model1;
    Example::ModelPtr<double> model2;
    model1->SetName("model1");
    model2->SetName("model2");

    model_vector->PushBack(model1);
    model_vector->PushBack(model2);
    dump(model_vector);

    std::cout << model_vector.GetA() << std::endl;

    return EXIT_SUCCESS;
}
