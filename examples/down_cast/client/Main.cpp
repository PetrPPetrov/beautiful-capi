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

#define EXAMPLE_CAPI_USE_DYNAMIC_LOADER
#define EXAMPLE_CAPI_DEFINE_FUNCTION_POINTERS
#include "Example.h"

using Example::down_cast;

void show(Example::IShapePtr shape)
{
    shape->Show();
    if (down_cast<Example::IPolygonPtr>(shape)->IsNotNull())
    {
        std::cout << "IPolygon" << std::endl;
        Example::IPolygonPtr polygon = down_cast<Example::IPolygonPtr>(shape);
        std::cout << "number of points = " << polygon->GetPointsCount() << std::endl;
    }
    if (down_cast<Example::ITrianglePtr>(shape)->IsNotNull())
    {
        std::cout << "ITriangle" << std::endl;
        Example::ITrianglePtr triangle = down_cast<Example::ITrianglePtr>(shape);
        triangle->SetPoints(-1, 1, 5, 6, 10, 15);
    }
    if (down_cast<Example::ISquarePtr>(shape)->IsNotNull())
    {
        std::cout << "ISquare" << std::endl;
        Example::ISquarePtr square = down_cast<Example::ISquarePtr>(shape);
        square->SetSize(3.14);
    }
    if (down_cast<Example::ICirclePtr>(shape)->IsNotNull())
    {
        std::cout << "ICircle" << std::endl;
        Example::ICirclePtr circle = down_cast<Example::ICirclePtr>(shape);
        circle->SetRadius(7.77);
    }
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
#ifdef _WIN32
    Example::Initialization module_init("down_cast.dll");
#elif __APPLE__
    Example::Initialization module_init("libdown_cast.dylib");
#else
    Example::Initialization module_init("libdown_cast.so");
#endif

    Example::IShapePtr triangle = Example::CreateTriangle();
    Example::IShapePtr shape0(Example::CreateCircle());
    Example::IShapePtr shape1(Example::CreateSquare());

    std::cout << std::endl << "The first pass." << std::endl;
    show(triangle);
    show(shape0);
    show(shape1);

    std::cout << std::endl << "The second pass." << std::endl;
    show(triangle);
    show(shape0);
    show(shape1);

    std::cout << std::endl;
    return EXIT_SUCCESS;
}
