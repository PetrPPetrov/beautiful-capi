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

#ifndef BEAUTIFUL_CAPI_DEFAULT_PRINTER_H
#define BEAUTIFUL_CAPI_DEFAULT_PRINTER_H

#include "IPrinter.h"
#include "Exception/BadArgumentImpl.h"

namespace Example
{
    class PrinterBaseImpl : public IPrinter
    {
        int mRefCount;
    public:
        PrinterBaseImpl();
        PrinterBaseImpl(const PrinterBaseImpl& other);
        virtual ~PrinterBaseImpl(); // Virtual destructor is required here
        virtual void AddRef();
        virtual void Release();
    };

    class DefaultPrinterImpl : public PrinterBaseImpl
    {
        Example::EQuality mQuality;
    public:
        DefaultPrinterImpl();
        DefaultPrinterImpl(const DefaultPrinterImpl& other);
        ~DefaultPrinterImpl();
        virtual void Print(const char* text) const;
        virtual void SetPrintingQuality(Example::EQuality quality);
        virtual Example::EQuality GetPrintingQuality() const;
        virtual Example::EPrintingDevice GetDeviceType() const;
    };

    inline DefaultPrinterImpl* CreateDefaultPrinterImpl(Example::EPrintingDevice printing_device)
    {
        if (printing_device == Example::printer)
        {
            return new DefaultPrinterImpl();
        }
        else
        {
            throw Exception::BadArgumentImpl("Can't create any other device except printers!", "printing_device");
        }
    }
}

#endif /* BEAUTIFUL_CAPI_DEFAULT_PRINTER_H */
