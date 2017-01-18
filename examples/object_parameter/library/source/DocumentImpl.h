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

#ifndef BEAUTIFUL_CAPI_DOCUMENT_H
#define BEAUTIFUL_CAPI_DOCUMENT_H

#include "PageImpl.h"

namespace Example
{
    class DocumentImpl
    {
        int mRefCount;
        PageImpl* mPage; // better to use a smart-pointer here, but for this example (for simpilicity) we use raw pointer and manually call AddRef()\Release()
    public:
        DocumentImpl();
        DocumentImpl(const DocumentImpl& other);
        ~DocumentImpl();

        void AddRef();
        void Release();

        void Show() const;
        PageImpl* GetPage() const;
        void SetPage(PageImpl* page);
    };

    inline void intrusive_ptr_add_ref(DocumentImpl* document)
    {
        if (document)
        {
            document->AddRef();
        }
    }

    inline void intrusive_ptr_release(DocumentImpl* document)
    {
        if (document)
        {
            document->Release();
        }
    }
}

#endif /* BEAUTIFUL_CAPI_DOCUMENT_H */
