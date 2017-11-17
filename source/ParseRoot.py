#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2016 Petr Petrovich Petrov
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

import os
from xml.dom.minidom import parse as dom_parse

from Parser import load


def get_all_namespaces(root_namespaces: list):
    result = root_namespaces.copy()
    for namespace in root_namespaces:
        result += get_all_namespaces(namespace.namespaces)
    return result

def parse_root(root_api_xml_path: str):
    root_api = load(dom_parse(root_api_xml_path))
    namespaces = get_all_namespaces(root_api.namespaces)

    cur_dir = os.path.dirname(root_api_xml_path)
    for namespace in namespaces:
        for include in namespace.includes:
            path = os.path.normpath(os.path.join(cur_dir, include.path))
            if os.path.exists(path):
                sub_api = parse_root(path)

                def update_attr(source, destination, attr_name: str):
                    if hasattr(source, attr_name) and hasattr(destination, attr_name):
                        dst_attr = getattr(destination, attr_name)
                        used_names = [element.name for element in dst_attr]
                        src_attr = getattr(source, attr_name)
                        for sub_element in src_attr:
                            sub_name = sub_element.name
                            if sub_name in used_names:
                                print("WARNING: {path} namespace {root} already contains {sub}; "
                                      "skipping import from {include}".format(
                                    root=destination.name, sub=sub_name, path=root_api_xml_path, include=path
                                ))
                            else:
                                dst_attr.append(sub_element)
                                used_names.append(sub_name)

                if include.use_content_without_root_namespaces:
                    for sub_api_nested_ns in sub_api.namespaces:
                        update_attr(sub_api_nested_ns, namespace, 'namespaces')
                        update_attr(sub_api_nested_ns, namespace, 'classes')
                        update_attr(sub_api_nested_ns, namespace, 'functions')
                else:
                    update_attr(sub_api, namespace, 'namespaces')

    return root_api
