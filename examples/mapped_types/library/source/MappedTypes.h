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

#ifndef BEAUTIFUL_CAPI_HELLO_WORLD_PRINTER_H
#define BEAUTIFUL_CAPI_HELLO_WORLD_PRINTER_H
#include <string>
namespace MappedTypes
{
    class PersonImpl
    {
    private:
        std::string firstName;
        const char* secondName;        
        int age;
        bool isMan;
    public:        
        const std::string& GetFirstName() const;
        void SetFirstName(const std::string&);
        const char* GetSecondName() const;
        void SetSecondName(const char*);
        int GetAge() const;
        void SetAge(int);
        bool IsMan() const;
        void SetSex(bool);
    };
    
    class DeviceImpl
    {
    private:
        std::string name;
        bool isBusy;
    public:        
        const std::string& GetName() const;
        void SetName(const std::string&);
        bool IsBusy() const;
        void SetBusy(bool);
    };
    
}

#endif /* BEAUTIFUL_CAPI_HELLO_WORLD_PRINTER_H */
