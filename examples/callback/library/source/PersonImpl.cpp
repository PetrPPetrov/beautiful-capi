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

#include <sstream>
#include <iostream>
#include "PersonImpl.h"
#include "Exception/GenericImpl.h"
#include "Exception/BadArgumentImpl.h"
#include "Exception/DivisionByZeroImpl.h"
#include "Exception/NullArgumentImpl.h"

Example::PersonImpl::PersonImpl()
{
}

Example::PersonImpl::PersonImpl(const PersonImpl& other_person)
    : first_name(other_person.first_name),
    second_name(other_person.second_name),
    age(other_person.age),
    sex(other_person.sex)
{
}

void Example::PersonImpl::SetFirstName(const char* first_name)
{
    this->first_name = first_name;
}

const char* Example::PersonImpl::GetFirstName() const
{
    return this->first_name.c_str();
}

void Example::PersonImpl::SetSecondName(const char* second_name)
{
    this->second_name = second_name;
}

const char* Example::PersonImpl::GetSecondName() const
{
    return this->second_name.c_str();
}

void Example::PersonImpl::SetAge(unsigned int age)
{
    this->age = age;
}

unsigned int Example::PersonImpl::GetAge() const
{
    return this->age;
}

void Example::PersonImpl::SetSex(Example::PersonImpl::ESex sex)
{
    this->sex = sex;
}

Example::PersonImpl::ESex Example::PersonImpl::GetSex() const
{
    return sex;
}

void Example::PersonImpl::Dump(Example::IPrinter* printer) const
{
    class print_helper : public std::stringstream
    {
        Example::IPrinter *mPrinter;
    public:
        print_helper(Example::IPrinter *printer) : mPrinter(printer) {}
        ~print_helper()
        {
            if (mPrinter)
            {
                mPrinter->Print(str().c_str());
            }
        }
    };

    print_helper printer_io(printer);
    printer_io << "First Name: " << this->first_name << " Second Name: " << this->second_name << " Age: " << this->age << " Sex: " << (this->male ? "M" : "F");
}

void Example::PersonImpl::Print(Example::IPrinter* printer, const char* text) const
{
    try
    {
        printer->Print(text);
    }
    catch (Exception::NullArgumentImpl& null_argument_exception)
    {
        std::cout << "    *** Exception::NullArgument was thrown" << std::endl;
        std::cout << "    " << null_argument_exception.GetErrorText() << std::endl;
        std::cout << "    argument: " << null_argument_exception.GetArgumentName() << std::endl;
    }
    catch (Exception::BadArgumentImpl& null_argument_exception)
    {
        std::cout << "    *** Exception::BadArgument was thrown" << std::endl;
        std::cout << "    " << null_argument_exception.GetErrorText() << std::endl;
    }
    catch (Exception::GenericImpl& generic_exception)
    {
        std::cout << "    *** Exception::Generic was thrown" << std::endl;
        std::cout << "    " << generic_exception.GetErrorText() << std::endl;
    }
    catch (const std::exception& exception)
    {
        std::cout << "    *** std::exception was thrown" << std::endl;
        std::cout << "    " << exception.what() << std::endl;
    }
    catch (...)
    {
        std::cout << "    *** Unknown exception was hrown" << std::endl;
    }
}
