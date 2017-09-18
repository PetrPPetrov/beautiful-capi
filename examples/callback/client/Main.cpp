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

#if defined(_WIN32) && defined(_DEBUG)
#include <crtdbg.h>
#endif
#include <cctype>
#include <iostream>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <stdint.h>
#include "Example.h"

class CustomPrinterImplementation
{
    mutable std::string mLastPrintedText;
    Example::PrinterPtr::EQuality mQuality;
public:
    CustomPrinterImplementation()
    {
        std::cout << "CustomPrinterImplementation ctor" << std::endl;
    }
    ~CustomPrinterImplementation()
    {
        std::cout << "CustomPrinterImplementation dtor" << std::endl;
    }
    void Print(const char* text) const // Note that this method is non-virtual
    {
        if (!text)
        {
            // This exception will be correctly passed through the library boundary
            // and will be caught by the library code
            throw Exception::NullArgument();
        }
        mLastPrintedText = std::string(text);
        std::transform(mLastPrintedText.begin(), mLastPrintedText.end(), mLastPrintedText.begin(), toupper);
        std::cout << mLastPrintedText << std::endl;
    }
    void SetPrintingQuality(Example::PrinterPtr::EQuality printing_quality)
    {
        mQuality = printing_quality;
    }
    Example::PrinterPtr::EQuality GetPrintingQuality() const
    {
        return mQuality;
    }
    Example::EPrintingDevice GetDeviceType() const
    {
        return Example::printer;
    }
};

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Example::Person famous_person;
    famous_person.SetFirstName("Isaac");
    famous_person.SetSecondName("Newton");
    famous_person.SetAge(26);
    famous_person.SetSex(Example::Person::male);

    Example::PrinterPtr printing_device = Example::CreateDefaultPrinter(Example::printer);
    famous_person.Dump(printing_device);
    famous_person.Print(printing_device, "Hello World");

    CustomPrinterImplementation my_printer_implementation;
    printing_device = Example::create_callback_for_printer(my_printer_implementation);
    famous_person.Dump(printing_device);

    // CustomPrinterImplementation::Print() will throw exception (Exception::NullArgument)
    // and this exception will be caught by the library code
    famous_person.Print(printing_device, 0);

    return EXIT_SUCCESS;
}
