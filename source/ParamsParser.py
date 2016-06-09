#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2015 Petr Petrovich Petrov
#
# This file is part of Beautiful Capi.
#
# Beautiful Capi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Beautiful Capi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
#


#
# WARNING: This file was automatically generated by Xsd2Python3.py program!
# Do not edit this file! Please edit the source XSD schema.
#


from enum import Enum


def string_to_bool(string_value):
    return string_value.lower() in ["true", "on", "yes", "1"]


class TBeautifulCapiParams(object):
    def __init__(self):
        self.m_folder_per_namespace = True
        self.m_file_per_class = True
        self.m_namespace_header_at_parent_folder = True
        self.m_generate_single_file = False
        self.m_single_header_name = "Output.h"
        self.m_dynamically_load_functions = False
        self.m_capi_header_suffix = "Capi"
        self.m_fwd_header_suffix = "Fwd"
        self.m_wrapper_class_suffix = "Ptr"
        self.m_forward_typedef_suffix = "FwdPtr"
        self.m_is_null_method = "IsNull"
        self.m_is_not_null_method = "IsNotNull"
        self.m_delete_method = "Delete"
        self.m_copyright_header = ""
        self.m_automatic_generated_warning = ""
    
    def load(self, dom_node):
        for element in [node for node in dom_node.childNodes if node.nodeName == "copyright_header"]:
            for text in [text for text in element.childNodes if text.nodeType == text.TEXT_NODE]:
                self.m_copyright_header += text.nodeValue
        for element in [node for node in dom_node.childNodes if node.nodeName == "automatic_generated_warning"]:
            for text in [text for text in element.childNodes if text.nodeType == text.TEXT_NODE]:
                self.m_automatic_generated_warning += text.nodeValue
        if dom_node.hasAttribute("folder_per_namespace"):
            cur_attr = dom_node.getAttribute("folder_per_namespace")
            self.m_folder_per_namespace = string_to_bool(cur_attr)
        if dom_node.hasAttribute("file_per_class"):
            cur_attr = dom_node.getAttribute("file_per_class")
            self.m_file_per_class = string_to_bool(cur_attr)
        if dom_node.hasAttribute("namespace_header_at_parent_folder"):
            cur_attr = dom_node.getAttribute("namespace_header_at_parent_folder")
            self.m_namespace_header_at_parent_folder = string_to_bool(cur_attr)
        if dom_node.hasAttribute("generate_single_file"):
            cur_attr = dom_node.getAttribute("generate_single_file")
            self.m_generate_single_file = string_to_bool(cur_attr)
        if dom_node.hasAttribute("single_header_name"):
            cur_attr = dom_node.getAttribute("single_header_name")
            self.m_single_header_name = cur_attr
        if dom_node.hasAttribute("dynamically_load_functions"):
            cur_attr = dom_node.getAttribute("dynamically_load_functions")
            self.m_dynamically_load_functions = string_to_bool(cur_attr)
        if dom_node.hasAttribute("capi_header_suffix"):
            cur_attr = dom_node.getAttribute("capi_header_suffix")
            self.m_capi_header_suffix = cur_attr
        if dom_node.hasAttribute("fwd_header_suffix"):
            cur_attr = dom_node.getAttribute("fwd_header_suffix")
            self.m_fwd_header_suffix = cur_attr
        if dom_node.hasAttribute("wrapper_class_suffix"):
            cur_attr = dom_node.getAttribute("wrapper_class_suffix")
            self.m_wrapper_class_suffix = cur_attr
        if dom_node.hasAttribute("forward_typedef_suffix"):
            cur_attr = dom_node.getAttribute("forward_typedef_suffix")
            self.m_forward_typedef_suffix = cur_attr
        if dom_node.hasAttribute("is_null_method"):
            cur_attr = dom_node.getAttribute("is_null_method")
            self.m_is_null_method = cur_attr
        if dom_node.hasAttribute("is_not_null_method"):
            cur_attr = dom_node.getAttribute("is_not_null_method")
            self.m_is_not_null_method = cur_attr
        if dom_node.hasAttribute("delete_method"):
            cur_attr = dom_node.getAttribute("delete_method")
            self.m_delete_method = cur_attr
    

def load(dom_node):
    for root_element in [root for root in dom_node.childNodes if root.localName == "params"]:
        root_params = TBeautifulCapiParams()
        root_params.load(root_element)
        return root_params
