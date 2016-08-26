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

#ifndef BEAUTIFUL_CAPI_POINT_SET_POINTSET_H
#define BEAUTIFUL_CAPI_POINT_SET_POINTSET_H

#include "PointsImpl.h"
#include <string>
#include "boost/smart_ptr/intrusive_ptr.hpp"

namespace PointSet
{
    class PointSetImpl
    {
        boost::intrusive_ptr<PointsImpl> mPoints;
        std::string mName;
        int mRefCount;

    public:
        PointSetImpl() : mRefCount(1) {}

        const char* GetName() const { return mName.c_str(); }
        void SetName(const char* name) { mName = name; }

        PointsImpl* GetPoints() const { return mPoints.get(); }
        void SetPoints(PointsImpl* points) { mPoints = points; }

        void AddRef() { if (this) ++mRefCount; }
        void Release()
        {
            if (this)
            {
                --mRefCount;
                if (mRefCount <= 0)
                {
                    delete this;
                }
            }
        }
    };

    inline void intrusive_ptr_add_ref(PointSetImpl* printer)
    {
        printer->AddRef();
    }

    inline void intrusive_ptr_release(PointSetImpl* printer)
    {
        printer->Release();
    }
}

#endif /* BEAUTIFUL_CAPI_POINT_SET_POINTSET_H */
