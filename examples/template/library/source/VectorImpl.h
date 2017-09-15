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

#ifndef BEAUTIFUL_CAPI_TEMPLATE_VECTORIMPL_H
#define BEAUTIFUL_CAPI_TEMPLATE_VECTORIMPL_H

#include <vector>
#include <iostream>
#include "boost/intrusive_ptr.hpp"

namespace Example
{
    template<typename T>
    class VectorImpl
    {
        std::vector<T> mVector;
    public:
        VectorImpl()
        {
            std::cout << "Vector ctor" << std::endl;
        }
        VectorImpl(const VectorImpl& other) : mVector(other.mVector)
        {
            std::cout << "Vector copy ctor" << std::endl;
        }
        ~VectorImpl()
        {
            std::cout << "Vector dtor" << std::endl;
        }
        int GetSize() const
        {
            return static_cast<int>(mVector.size());
        }
        void Clear()
        {
            mVector.clear();
        }
        void PushBack(T value)
        {
            mVector.push_back(value);
        }
        T GetItem(int index) const
        {
            return mVector.at(static_cast<size_t>(index));
        }
    };

    class CharDummyVector
    {
    public:
        CharDummyVector()
        {
            std::cout << "CharDummyVector ctor" << std::endl;
        }
        CharDummyVector(const CharDummyVector& other)
        {
            std::cout << "CharDummyVector copy ctor" << std::endl;
        }
        ~CharDummyVector()
        {
            std::cout << "CharDummyVector dtor" << std::endl;
        }
        int GetSize() const
        {
            return 3;
        }
        void Clear()
        {
        }
        void PushBack(char value)
        {
        }
        char GetItem(int index) const
        {
            return 'A';
        }
    };

    template<typename T>
    struct smart_ptr : public boost::intrusive_ptr<T>
    {
        smart_ptr(T* smart_object) : boost::intrusive_ptr<T>(smart_object)
        {
        }
    };

    template<typename T>
    class VectorOfObjectsImpl
    {
        int mRefCount;
        std::vector<smart_ptr<T> > mVector;
    public:
        // By default newly created objects implies to have value 1 of reference counter
        VectorOfObjectsImpl() : mRefCount(1)
        {
            std::cout << "VectorOfObjects ctor" << std::endl;
        }
        // By default newly created objects implies to have value 1 of reference counter
        VectorOfObjectsImpl(const VectorOfObjectsImpl& other) : mRefCount(1), mVector(other.mVector)
        {
            std::cout << "VectorOfObjects copy ctor! (should be never called)" << std::endl;
        }
        virtual ~VectorOfObjectsImpl()
        {
            std::cout << "VectorOfObjects dtor" << std::endl;
        }
        int GetSize() const
        {
            return static_cast<int>(mVector.size());
        }
        void Clear()
        {
            mVector.clear();
        }
        void PushBack(smart_ptr<T> value)
        {
            mVector.push_back(value);
        }
        smart_ptr<T> GetItem(int index) const
        {
            return mVector.at(static_cast<size_t>(index));
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

    template<typename T>
    class VectorOfObjectsDerivedImpl : public VectorOfObjectsImpl<T>
    {
    public:
        // By default newly created objects implies to have value 1 of reference counter
        VectorOfObjectsDerivedImpl()
        {
            std::cout << "VectorOfObjectsDerivedImpl ctor" << std::endl;
        }
        // By default newly created objects implies to have value 1 of reference counter
        VectorOfObjectsDerivedImpl(const VectorOfObjectsDerivedImpl& other) : VectorOfObjectsImpl<T>(other)
        {
            std::cout << "VectorOfObjectsDerivedImpl copy ctor! (should be never called)" << std::endl;
        }
        virtual ~VectorOfObjectsDerivedImpl()
        {
            std::cout << "VectorOfObjectsDerivedImpl dtor" << std::endl;
        }
        int GetA() const
        {
            return 2;
        }
    };

    template<typename WorkType>
    inline void intrusive_ptr_add_ref(VectorOfObjectsImpl<WorkType>* objects)
    {
        if (objects)
        {
            objects->AddRef();
        }
    }

    template<typename WorkType>
    inline void intrusive_ptr_release(VectorOfObjectsImpl<WorkType>* objects)
    {
        if (objects)
        {
            objects->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_TEMPLATE_VECTORIMPL_H */
