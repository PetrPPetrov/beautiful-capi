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

#ifndef EXAMPLE_INCLUDED
#define EXAMPLE_INCLUDED

#include "ExampleCapi.h"
#include "ExampleFwd.h"
#include "ExampleEnums.h"
#include "Example/Printer.h"
#include "Example/Person.h"
#include "Example/PrinterCallback.h"
#include "Callback/common/check_and_throw_exception.h"

#ifdef __cplusplus

namespace Example {

/**
 * @brief Creates a default printing device.
 * @param printing_device specifies the printing device type.
 */
inline Example::PrinterPtr CreateDefaultPrinter(Example::EPrintingDevice printing_device)
{
    beautiful_capi_callback_exception_info_t exception_info;
    Example::PrinterPtr result(Example::PrinterPtr::force_creating_from_raw_pointer, example_create_default_printer(&exception_info, static_cast<int>(printing_device)), false);
    beautiful_capi_Callback::check_and_throw_exception(exception_info.code, exception_info.object_pointer);
    return result;
}
inline int GetMajorVersion()
{
    return example_get_major_version();
}
inline int GetMinorVersion()
{
    return example_get_minor_version();
}
inline int GetPatchVersion()
{
    return example_get_patch_version();
}

}

#endif /* __cplusplus */

#endif /* EXAMPLE_INCLUDED */

