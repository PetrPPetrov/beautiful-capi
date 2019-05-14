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

#ifndef BEAUTIFUL_CAPI_EXISTING_IMPL_H
#define BEAUTIFUL_CAPI_EXISTING_IMPL_H

#include <iostream>
namespace ApiInclude
{
    namespace ExistingNS
    {
        void SayHello();
    }

    class ExistingClassImpl
    {
    public:
        ExistingClassImpl() {}
        void SayHello();
    };

    void ExistingFunc();
}

#endif /* BEAUTIFUL_CAPI_EXISTING_IMPL_H */
