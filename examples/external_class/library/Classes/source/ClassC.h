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

#ifndef BEAUTIFUL_CAPI_CLASSES_CLASS_C_H
#define BEAUTIFUL_CAPI_CLASSES_CLASS_C_H

#include <string>
#include <iostream>

namespace Classes
{
    class ClassC
    {
        double mValue;        
        int mRefCount;   
    public:
        ClassC() : mRefCount(1), mValue(3.14) {}

        double GetValue() const
        {
            return mValue;
        }

        void SetValue(double value)
        {
            mValue = value;
        }

        void AddRef()
        {
            ++mRefCount;
        }

        void Release()
        {
            --mRefCount;
            if (mRefCount <= 0)
            {
                delete this;
            }
        }
    };

    inline void intrusive_ptr_add_ref(ClassC* object)
    {
        if (object)
        {
            object->AddRef();
        }
    }

    inline void intrusive_ptr_release(ClassC* object)
    {
        if (object)
        {
            object->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_CLASSES_CLASS_C_H */
