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

#ifndef BEAUTIFUL_CAPI_TRIANGLE_IMPL_H
#define BEAUTIFUL_CAPI_TRIANGLE_IMPL_H

#include "IPolygon.h"
#include "RefCountedImpl.h"

namespace Example
{
    class TriangleImpl : virtual public IPolygon, public RefCountedImpl
    {
        double m_x1, m_y1;
        double m_x2, m_y2;
        double m_x3, m_y3;
    public:
        TriangleImpl();
        TriangleImpl(const TriangleImpl& other);
        virtual ~TriangleImpl();
        virtual void Show() const;
        virtual int GetPointsCount() const;
        virtual void SetPoints(double x1, double y1, double x2, double y2, double x3, double y3);
    };
}

#endif /* BEAUTIFUL_CAPI_TRIANGLE_IMPL_H */
