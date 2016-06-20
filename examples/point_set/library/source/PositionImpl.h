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

#ifndef BEAUTIFUL_CAPI_POINT_SET_POSITION_H
#define BEAUTIFUL_CAPI_POINT_SET_POSITION_H

namespace PointSet
{
    class PositionImpl
    {
        double mX;
        double mY;
        double mZ;

    public:
        PositionImpl() : mX(0), mY(0), mZ(0) {}
        PositionImpl(double x, double y, double z) : mX(x), mY(y), mZ(z) {}
        PositionImpl(const PositionImpl& other) : mX(other.GetX()), mY(other.GetY()), mZ(other.GetZ()) {}

        double GetX() const { return mX; }
        double GetY() const { return mY; }
        double GetZ() const { return mZ; }

        void SetX(double value) { mX = value; }
        void SetY(double value) { mY = value; }
        void SetZ(double value) { mZ = value; }

    };
}

#endif /* BEAUTIFUL_CAPI_POINT_SET_POSITION_H */
