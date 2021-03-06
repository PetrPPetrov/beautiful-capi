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

#include <stdexcept>
#include <cassert>
#include "TriangleFactory.h"
#include "SquareFactory.h"
#include "CircleFactory.h"
#include "IShape.h"
#include "IPolygon.h"
#include "TriangleImpl.h"
#include "SquareImpl.h"
#include "CircleImpl.h"

#ifdef _WIN32
    #ifdef __GNUC__
        #define EXAMPLE_API extern "C" __attribute__ ((dllexport))
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else
        #define EXAMPLE_API extern "C" __declspec(dllexport)
        #define EXAMPLE_API_CONVENTION __cdecl
    #endif
#elif __APPLE__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API extern "C"
    #endif
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#elif __unix__ || __linux__
    #if defined(__GNUC__) && __GNUC__ >= 4
        #define EXAMPLE_API extern "C" __attribute__ ((visibility ("default")))
    #else
        #define EXAMPLE_API extern "C"
    #endif
    #ifdef __i386__
        #define EXAMPLE_API_CONVENTION __attribute__ ((cdecl))
    #else /* __i386__ */
        #define EXAMPLE_API_CONVENTION
    #endif /* __i386__ */
#else
    #error "Unknown platform"
#endif

int AutoGen_Internal_DownCast_ExampleGetMajorVersionImpl()
{
    return 1;
}

int AutoGen_Internal_DownCast_ExampleGetMinorVersionImpl()
{
    return 0;
}

int AutoGen_Internal_DownCast_ExampleGetPatchVersionImpl()
{
    return 0;
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_create_triangle()
{
    return Example::CreateTriangle();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_create_square()
{
    return Example::CreateSquare();
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_create_circle()
{
    return Example::CreateCircle();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_major_version()
{
    return AutoGen_Internal_DownCast_ExampleGetMajorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_minor_version()
{
    return AutoGen_Internal_DownCast_ExampleGetMinorVersionImpl();
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_get_patch_version()
{
    return AutoGen_Internal_DownCast_ExampleGetPatchVersionImpl();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_ishape_show_const(void* object_pointer)
{
    const Example::IShape* self = static_cast<Example::IShape*>(object_pointer);
    self->Show();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_ishape_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::IShape*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_ishape_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::IShape*>(object_pointer));
}

EXAMPLE_API int EXAMPLE_API_CONVENTION example_ipolygon_get_points_count_const(void* object_pointer)
{
    const Example::IPolygon* self = static_cast<Example::IPolygon*>(object_pointer);
    return self->GetPointsCount();
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_ipolygon_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::IPolygon*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_ipolygon_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::IPolygon*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ipolygon_cast_to_base(void* object_pointer)
{
    return static_cast<Example::IShape*>(static_cast<Example::IPolygon*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ishape_cast_to_example_ipolygon(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::IPolygon*>(static_cast<Example::IShape*>(source_object));
    }
    else
    {
        return 0;
    }
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_itriangle_set_points(void* object_pointer, double x1, double y1, double x2, double y2, double x3, double y3)
{
    Example::TriangleImpl* self = static_cast<Example::TriangleImpl*>(object_pointer);
    self->SetPoints(x1, y1, x2, y2, x3, y3);
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_itriangle_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::TriangleImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_itriangle_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::TriangleImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_itriangle_cast_to_base(void* object_pointer)
{
    return static_cast<Example::IPolygon*>(static_cast<Example::TriangleImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ishape_cast_to_example_itriangle(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::TriangleImpl*>(static_cast<Example::IShape*>(source_object));
    }
    else
    {
        return 0;
    }
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ipolygon_cast_to_example_itriangle(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::TriangleImpl*>(static_cast<Example::IPolygon*>(source_object));
    }
    else
    {
        return 0;
    }
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_isquare_set_size(void* object_pointer, double size)
{
    Example::SquareImpl* self = static_cast<Example::SquareImpl*>(object_pointer);
    self->SetSize(size);
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_isquare_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::SquareImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_isquare_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::SquareImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_isquare_cast_to_base(void* object_pointer)
{
    return static_cast<Example::IPolygon*>(static_cast<Example::SquareImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ishape_cast_to_example_isquare(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::SquareImpl*>(static_cast<Example::IShape*>(source_object));
    }
    else
    {
        return 0;
    }
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ipolygon_cast_to_example_isquare(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::SquareImpl*>(static_cast<Example::IPolygon*>(source_object));
    }
    else
    {
        return 0;
    }
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_icircle_set_radius(void* object_pointer, double radius)
{
    Example::CircleImpl* self = static_cast<Example::CircleImpl*>(object_pointer);
    self->SetRadius(radius);
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_icircle_add_ref(void* object_pointer)
{
    intrusive_ptr_add_ref(static_cast<Example::CircleImpl*>(object_pointer));
}

EXAMPLE_API void EXAMPLE_API_CONVENTION example_icircle_release(void* object_pointer)
{
    intrusive_ptr_release(static_cast<Example::CircleImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_icircle_cast_to_base(void* object_pointer)
{
    return static_cast<Example::IShape*>(static_cast<Example::CircleImpl*>(object_pointer));
}

EXAMPLE_API void* EXAMPLE_API_CONVENTION example_ishape_cast_to_example_icircle(void* source_object)
{
    if (source_object)
    {
        return dynamic_cast<Example::CircleImpl*>(static_cast<Example::IShape*>(source_object));
    }
    else
    {
        return 0;
    }
}
