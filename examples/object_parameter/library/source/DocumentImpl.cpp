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

#include <iostream>
#include "DocumentImpl.h"

// By default newly created objects implies to have value 1 of reference counter
Example::DocumentImpl::DocumentImpl() : mRefCount(1), mPage(0)
{
    std::cout << "Document ctor" << std::endl;
}

// By default newly created objects implies to have value 1 of reference counter
Example::DocumentImpl::DocumentImpl(const DocumentImpl& other) : mRefCount(1), mPage(other.mPage)
{
    std::cout << "Document copy ctor! (should be never called)" << std::endl;
    mPage->AddRef();
}

Example::DocumentImpl::~DocumentImpl()
{
    std::cout << "Document dtor" << std::endl;
    mPage->Release();
}

void Example::DocumentImpl::AddRef()
{
    ++mRefCount;
}

void Example::DocumentImpl::Release()
{
    --mRefCount;
    if (mRefCount <= 0)
    {
        delete this;
    }
}

void Example::DocumentImpl::Show() const
{
    std::cout << "Document show()" << std::endl;
    if (mPage)
    {
        std::cout << "Document has " << mPage->GetWidth() << " x " << mPage->GetHeight() << " page" << std::endl;
    }
    else
    {
        std::cout << "Document is empty" << std::endl;
    }
}

Example::PageImpl* Example::DocumentImpl::GetPage() const
{
    mPage->AddRef(); // We return a raw pointer, so, we need to call AddRef() here
    return mPage;
}

void Example::DocumentImpl::SetPage(PageImpl* page)
{
    page->AddRef();
    intrusive_ptr_release(mPage);
    mPage = page;
}
