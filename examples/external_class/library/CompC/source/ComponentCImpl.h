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

#ifndef BEAUTIFUL_CAPI_COMP_C_COMPONENT_C_H
#define BEAUTIFUL_CAPI_COMP_C_COMPONENT_C_H

#include <stdint.h>
#include <string>
#include <iostream>
#include "Classes.h"
#include "Classes/ClassC.h"

enum EAlign { Left, Right, Center };

namespace CompC
{    
    class ComponentC
    {
        Classes::ClassA mA;
        Classes::ClassBRawPtr mB;
        Classes::ClassCPtr mC;
        EAlign mD;
        int mRefCount;        
            
    public:
        // By default newly created objects implies to have value 1 of reference counter
        ComponentC() : mRefCount(1) {}

        const Classes::ClassA& GetA() const
        {
            return mA;
        }

        void SetA(const Classes::ClassA& a)
        {
            mA = a;
        }

        Classes::ClassBRawPtr GetB() const
        {
            return mB;
        }

        void SetB(Classes::ClassBRawPtr b)
        {
            mB->Delete();
            mB = b;
        }

        Classes::ClassCPtr GetC() const
        {
            return mC;
        }

        void SetC(Classes::ClassCPtr c)
        {
            mC = c;
        }

        EAlign GetD() const
        {
            return mD;
        }

        void SetD(EAlign d)
        {
            mD = d;
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
    
    inline void intrusive_ptr_add_ref(ComponentC* object)
    {
        if (object)
        {
            object->AddRef();
        }
    }

    inline void intrusive_ptr_release(ComponentC* object)
    {
        if (object)
        {
            object->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_COMP_C_COMPONENT_C_H */
