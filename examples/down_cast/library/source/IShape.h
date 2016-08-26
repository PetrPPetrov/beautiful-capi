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

#ifndef BEAUTIFUL_CAPI_ISHAPE_H
#define BEAUTIFUL_CAPI_ISHAPE_H

#include <string>

namespace Example
{
    struct IShape
    {
        virtual ~IShape() {} // virtual destructor is required here
        virtual void Show() const = 0;
        virtual void AddRef() = 0;
        virtual void Release() = 0;
    };

    inline void intrusive_ptr_add_ref(IShape* ref_counted_shape)
    {
        ref_counted_shape->AddRef();
    }

    inline void intrusive_ptr_release(IShape* ref_counted_shape)
    {
        ref_counted_shape->Release();
    }
}

#endif /* BEAUTIFUL_CAPI_ISHAPE_H */
