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

import Parser
from Constants import Constants
from TraitsBase import TraitsBase


class LifecycleTraitsBase(TraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_delete_destructor(self):
        self.put_line('~{class_name}()'.format(class_name=self.interface.m_name))
        self.put_line('{')
        with self.indent():
            self.put_line('if ({object_var})'.format(object_var=Constants.object_var))
            self.put_line('{')
            with self.indent():
                self.put_line('{delete_c_function}({object_var});'.format(
                    delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix,
                    object_var=Constants.object_var))
                self.put_line('SetObject(0);')
            self.put_line('}')
        self.put_line('}')
        self.put_source_line('{delete_c_function}(void* object_pointer);'.format(
            delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix))


class CopySemantic(LifecycleTraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_destructor(self):
        self.generate_delete_destructor()

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other)'.format(class_name=self.interface.m_name))
        self.put_line('{')
        with self.indent():
            self.put_line('SetObject({copy_c_function}(other.{object_var}));'.format(
                copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix,
                object_var=Constants.object_var))
        self.put_line('}')
        self.put_source_line('{copy_c_function}(void* object_pointer});'.format(
            copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix))


class MoveSemantic(LifecycleTraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_destructor(self):
        self.generate_delete_destructor()

    def generate_copy_constructor(self):
        self.put_line('{class_name}({class_name}& other)'.format(class_name=self.interface.m_name))
        self.put_line('{')
        with self.indent():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
            self.put_line('other.SetObject(0);')
        self.put_line('}')


class RefCountedSemantic(LifecycleTraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_destructor(self):
        if not self.interface.m_base:
            self.put_line('~{class_name}()'.format(class_name=self.interface.m_name))
            self.put_line('{')
            with self.indent():
                self.put_line('if ({object_var})'.format(
                    object_var=Constants.object_var))
                self.put_line('{')
                with self.indent():
                    self.put_line('{release_c_function}({object_var});'.format(
                        release_c_function=self.capi_generator.get_namespace_id().lower() + Constants.release_suffix,
                        object_var=Constants.object_var))
                self.put_line('}')
            self.put_line('}')
            self.put_source_line('{release_c_function}(void* object_pointer);'.format(
                release_c_function=self.capi_generator.get_namespace_id().lower() + Constants.release_suffix))

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other)'.format(class_name=self.interface.m_name))
        self.put_line('{')
        with self.indent():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
            self.put_line('{addref_c_function}({object_var});'.format(
                addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.addref_suffix,
                object_var=Constants.object_var))
        self.put_line('}')
        self.put_source_line('{addref_c_function}(void* object_pointer);'.format(
            addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.addref_suffix))


str_to_lifecycle = {
    Parser.TLifecycle.copy_semantic: CopySemantic,
    Parser.TLifecycle.move_semantic: MoveSemantic,
    Parser.TLifecycle.reference_counted: RefCountedSemantic
}


def create_lifecycle_traits(interface, capi_generator):
    if interface.m_lifecycle in str_to_lifecycle:
        return str_to_lifecycle[interface.m_lifecycle](interface, capi_generator)
    raise ValueError
