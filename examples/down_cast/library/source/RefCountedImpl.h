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

#ifndef BEAUTIFUL_CAPI_REFCOUNTED_IMPL_H
#define BEAUTIFUL_CAPI_REFCOUNTED_IMPL_H

#include "IShape.h"

#ifdef _MSC_VER
#pragma warning(disable: 4250)
#endif

namespace Example
{
    class RefCountedImpl : virtual public IShape
    {
        int mRefCount;
    public:
        // By default newly created objects implies to have value 1 of reference counter
        RefCountedImpl() : mRefCount(1)
        {
        }

        // Virtual destructor is required here
        virtual ~RefCountedImpl()
        {
            mRefCount = 0;
        }

        virtual void AddRef()
        {
            ++mRefCount;
        }

        virtual void Release()
        {
            --mRefCount;
            if (mRefCount <= 0)
            {
                delete this;
            }
        }
    };
}

#endif /* BEAUTIFUL_CAPI_REFCOUNTED_IMPL_H */
