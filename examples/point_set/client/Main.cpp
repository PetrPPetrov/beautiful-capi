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
#include "PointSet.h"

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    PointSet::PointSetPtr set;
    set.SetName("Points");
    {
        PointSet::PointsPtr points;
        points.Reserve(3);
        points.PushBack( PointSet::Position(1, 0, 0) );
        points.PushBack( PointSet::Position(0, 1, 0) );
        points.PushBack( PointSet::Position(0, 0, 1) );
        set.SetPoints(points);
    }

    {
        std::cout << "PointSet '" << set.GetName() << "'" << std::endl;

        PointSet::PointsPtr points = set.GetPoints();

        for (size_t i = 0; i < points->Size() ; ++i)
        {
            PointSet::Position pos = points->GetElement(i);
            std::cout << "\tpoint #" << i << " ("<< pos.GetX() << ", " << pos.GetY() << ", " << pos.GetZ() << ")" << std::endl;
        }
    }
    return EXIT_SUCCESS;
}
