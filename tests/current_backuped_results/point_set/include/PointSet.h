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

/*
 * WARNING: This file was automatically generated by Beautiful Capi!
 * Do not edit this file! Please edit the source API description.
 */

#ifndef POINTSET_INCLUDED
#define POINTSET_INCLUDED

#include "PointSetCapi.h"
#include "PointSetFwd.h"
#include "PointSet/Position.h"
#include "PointSet/Points.h"
#include "PointSet/PointSet.h"

#ifdef __cplusplus

namespace PointSet {

inline int GetMajorVersion()
{
    return point_set_get_major_version();
}
inline int GetMinorVersion()
{
    return point_set_get_minor_version();
}
inline int GetPatchVersion()
{
    return point_set_get_patch_version();
}

}

#endif /* __cplusplus */

#endif /* POINTSET_INCLUDED */

