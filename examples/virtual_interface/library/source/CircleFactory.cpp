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
#include "CircleFactory.h"

namespace Example
{
    namespace Details
    {
        class Circle : public Example::IShape
        {
        public:
            Circle()
            {
                std::cout << "Circle ctor" << std::endl;
            }

            Circle(const Circle& other)
            {
                std::cout << "Circle copy ctor" << std::endl;
            }

            virtual ~Circle()
            {
                std::cout << "Circle dtor" << std::endl;
            }

            virtual void Show() const
            {
                std::cout << "Circle::Show()" << std::endl;
            }
        };
    }
}

Example::IShape* Example::Details::CreateCircle()
{
    return new Example::Details::Circle();
}
