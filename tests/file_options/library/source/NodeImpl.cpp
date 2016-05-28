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
#include "NodeImpl.h"

Example::Scene::NodeImpl::NodeImpl()
{
    std::cout << "Node ctor" << std::endl;
}

Example::Scene::NodeImpl::NodeImpl(const Example::Scene::NodeImpl& other)
    : mName(other.mName)
{
    std::cout << "Node copy ctor" << std::endl;
}

Example::Scene::NodeImpl::~NodeImpl()
{
    std::cout << "Node dtor" << std::endl;
}

const char* Example::Scene::NodeImpl::GetName() const
{
    return mName.c_str();
}

void Example::Scene::NodeImpl::SetName(const char* value)
{
    mName = value;
}
