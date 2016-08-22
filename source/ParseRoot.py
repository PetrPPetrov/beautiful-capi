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

import ParamsParser
import Parser

import os
from xml.dom.minidom import parse as dom_parse


def __get_all_namespaces(root_namespaces: list):
    result = root_namespaces.copy()
    for namespace in root_namespaces:
        result += __get_all_namespaces(namespace.namespaces)
    return result


def parse_root(root_api_xml_path: str):
    root_api = Parser.load(dom_parse(root_api_xml_path))
    namespaces = __get_all_namespaces(root_api.namespaces)

    cur_dir = os.path.dirname(root_api_xml_path)
    for namespace in namespaces:
        for include in namespace.includes:
            path = os.path.normpath(os.path.join(cur_dir, include.path))
            if os.path.exists(path):
                 sub_api = parse_root(path)
                 used_names = [ns.name for ns in namespace.namespaces]
                 for sub_namespace in sub_api.namespaces:
                     sub_name = sub_namespace.name
                     if sub_name in used_names:
                         print("WARNING: {path} namespace {root} already contains {sub} namespace; skipping import from {include}".format(
                             root = namespace.name, sub=sub_name, path=root_api_xml_path, include=path
                         ))
                     else:
                         namespace.namespaces.append(sub_namespace)
                         used_names.append(sub_name)

    return root_api
