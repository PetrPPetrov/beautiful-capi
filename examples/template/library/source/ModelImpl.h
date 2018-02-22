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

#ifndef BEAUTIFUL_CAPI_TEMPLATE_MODELIMPL_H
#define BEAUTIFUL_CAPI_TEMPLATE_MODELIMPL_H

#include <vector>
#include <iostream>
#include "PositionImpl.h"

namespace Example
{
    template<typename WorkType>
    class ModelImpl
    {
        int mRefCount;
        Example::PositionImpl<WorkType> mPosition;
        std::string mName;

    public:
        // By default newly created objects implies to have value 1 of reference counter
        ModelImpl() : mRefCount(1)
        {
            std::cout << "Model ctor" << std::endl;
        }
        // By default newly created objects implies to have value 1 of reference counter
        ModelImpl(const ModelImpl& other) : mRefCount(1), mPosition(other.mPoints)
        {
            std::cout << "Model copy ctor! (should be never called)" << std::endl;
        }
        ~ModelImpl()
        {
            std::cout << "Model dtor" << std::endl;
        }
        const char* GetName() const
        {
            return mName.c_str();
        }
        void SetName(const char* name)
        {
            mName = name;
        }
        Example::PositionImpl<WorkType> GetPosition() const
        {
            return mPosition;
        }
        void SetPosition(Example::PositionImpl<WorkType> position)
        {
            mPosition = position;
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
        template <typename WorkType> friend std::ostream& operator<<(std::ostream& os, const ModelImpl<WorkType>& position);
        void dump() const
        {
            std::cout << *this;
        }
    };

    template <typename WorkType> std::ostream& operator<<(std::ostream& os, const ModelImpl<WorkType>& model)
    {
        os << "model name = " << model.GetName() << std::endl;
        os << "model position:" << std::endl; 
        os << model.GetPosition() << std::endl;
        return os;
    }

    template<typename WorkType>
    inline void intrusive_ptr_add_ref(ModelImpl<WorkType>* model)
    {
        if (model)
        {
            model->AddRef();
        }
    }

    template<typename WorkType>
    inline void intrusive_ptr_release(ModelImpl<WorkType>* model)
    {
        if (model)
        {
            model->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_TEMPLATE_MODELIMPL_H */
