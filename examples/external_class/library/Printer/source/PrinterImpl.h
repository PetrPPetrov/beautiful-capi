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

#ifndef BEAUTIFUL_CAPI_PRINTER_N_S_PRINTER_H
#define BEAUTIFUL_CAPI_PRINTER_N_S_PRINTER_H

#include <iostream>
#include <string>
#include <vector>
#include <stddef.h>
#include "Components.h"
#include "CompC.h"

namespace PrinterNS
{
    class PrinterImpl
    {
    private:
        CompC::Align mAlign; 
        Components::EComponentType mType;
        
        
        std::string Align(std::string text)
        {
            std::string result = "";
            int indent = 0;
            if (mAlign == CompC::Right)
                indent = 80 - text.length();
            else if (mAlign == CompC::Center)            
                indent = (80 - text.length()) / 2;            
            for (int i = 0; i < indent; ++i)
                result += " ";
            result += text; 
            return result;
        }
        
        
    public:
        void Show(const Components::ComponentA& a)
        {
            std::ostringstream sstream;
            sstream << a.GetA().GetValue() << " " << a.GetB()->GetValue() << " " << a.GetC()->GetValue() << std::endl;
            std::cout << Align(sstream.str());
        }

        void Show(Components::ComponentBRawPtr b)
        {
            std::cout << b->GetA().GetValue() << " " << b->GetB()->GetValue() << " " << b->GetC()->GetValue()<< std::endl;
        }

        void Show(CompC::ComponentCPtr c)
        {
            std::cout << c->GetA().GetValue() << " " << c->GetB()->GetValue() << " " << c->GetC()->GetValue()<< std::endl;
        }
        
        CompC::ComponentCPtr GetCompC() const
        {
            return CompC::ComponentCPtr();
        }
        
        CompC::Align GetAlign() const
        {
            return mAlign;
        }
        
        void SetAlign(CompC::Align align)
        {
            mAlign = align;
        }
        
        Components::EComponentType GetComponentType() const
        {
            return mType;
        }
        
        void SetComponentType(Components::EComponentType type)
        {
            mType = type;
        }        
    };

    
}

#endif /* BEAUTIFUL_CAPI_PRINTER_N_S_PRINTER_H */
