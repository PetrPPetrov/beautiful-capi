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

#ifndef BEAUTIFUL_CAPI_TEMPLATE_POSITIONIMPL_H
#define BEAUTIFUL_CAPI_TEMPLATE_POSITIONIMPL_H

#include <vector>
#include <iostream>

namespace Example
{
    template<typename WorkType>
    class PositionImpl
    {
        WorkType mX, mY, mZ;
    public:
        PositionImpl() : mX(0), mY(0), mZ(0)
        {
            std::cout << "Position ctor" << std::endl;
        }
        PositionImpl(const PositionImpl& other) : mX(other.mX), mY(other.mY), mZ(other.mZ)
        {
            std::cout << "Position copy ctor" << std::endl;
        }
        ~PositionImpl()
        {
            std::cout << "Position dtor" << std::endl;
        }
        WorkType GetX() const
        {
            return mX;
        }
        void SetX(WorkType x)
        {
            mX = x;
        }
        WorkType GetY() const
        {
            return mY;
        }
        void SetY(WorkType y)
        {
            mY = y;
        }
        WorkType GetZ() const
        {
            return mZ;
        }
        void SetZ(WorkType z)
        {
            mZ = z;
        }
        template <typename WorkType> friend std::ostream& operator<<(std::ostream& os, const PositionImpl<WorkType>& dt);
        void dump() const
        {
            std::cout << *this;
        }
    };
    
    template <typename T> std::ostream& operator<<(std::ostream& os, const PositionImpl<T>& position)
    {
        os << "X: " << position.mX << std::endl;
        os << "Y: " << position.mY << std::endl;
        os << "Z: " << position.mZ << std::endl;
        return os;
    }

    template<typename WorkType>
    class Position4DImpl : public PositionImpl<WorkType>
    {
        WorkType mW;
    public:
        Position4DImpl() : mW(1)
        {
            std::cout << "Position4D ctor" << std::endl;
        }
        Position4DImpl(const Position4DImpl& other) : PositionImpl<WorkType>(other), mW(other.mW)
        {
            std::cout << "Position4D copy ctor" << std::endl;
        }
        ~Position4DImpl()
        {
            std::cout << "Position4D dtor" << std::endl;
        }
        WorkType GetW() const
        {
            return mW;
        }
        void SetW(WorkType w)
        {
            mW = w;
        }
        template <typename WorkType> friend std::ostream& operator<<(std::ostream& os, const Position4DImpl<WorkType>& position);
        void dump() const
        {
            std::cout << *this;
        }
    };

    template <typename T> std::ostream& operator<<(std::ostream& os, const Position4DImpl<T>& position)
    {
        os << (PositionImpl<T>)position;
        os << "W: " << position.mW << std::endl;
        return os;
    }
}

#endif /* BEAUTIFUL_CAPI_TEMPLATE_POSITIONIMPL_H */
