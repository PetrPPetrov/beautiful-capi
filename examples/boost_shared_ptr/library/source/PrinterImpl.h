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

#ifndef BEAUTIFUL_CAPI_PRINTER_H
#define BEAUTIFUL_CAPI_PRINTER_H

#include "boost/shared_ptr.hpp"
#include "boost/make_shared.hpp"

namespace Example
{
    class PrinterImpl
    {
    public:
        PrinterImpl();
        PrinterImpl(const PrinterImpl& other);
        ~PrinterImpl();
        void Show(const char* text) const;
    };

    class PrinterSharedPtr : public boost::shared_ptr<PrinterImpl>
    {
    public:
        PrinterSharedPtr() : boost::shared_ptr<PrinterImpl>(boost::make_shared<PrinterImpl>())
        {}
    };
}

#endif /* BEAUTIFUL_CAPI_PRINTER_H */
