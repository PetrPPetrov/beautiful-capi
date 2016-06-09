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
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_delete_destructor(self):
        self.put_line('~{class_name}()'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('{delete_c_function}({object_var});'.format(
                delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix,
                object_var=Constants.object_var
            ))
        c_function_declaration = 'void {delete_c_function}(void* object_pointer)'.format(
            delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('delete static_cast<{0}*>(object_pointer);'.format(
                self.cur_class.m_implementation_class_name
            ))
        self.put_source_line('')

    def generate_void_constructor(self):
        self.put_line('explicit {class_name}(void *object_pointer)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject(object_pointer);')
        self.put_line('bool {0}() const'.format(self.capi_generator.params_description.m_is_null_method))
        with self.indent_scope():
            self.put_line('return !{0};'.format(Constants.object_var))
        self.put_line('bool {0}() const'.format(self.capi_generator.params_description.m_is_not_null_method))
        with self.indent_scope():
            self.put_line('return {0} != 0;'.format(Constants.object_var))
        self.put_line('bool operator!() const')
        with self.indent_scope():
            self.put_line('return !{0};'.format(Constants.object_var))
        self.put_line('{class_name}* operator->()'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('return this;')
        self.put_line('const {class_name}* operator->() const'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('return this;')

    def generate_delete_method(self):
        pass


class CopySemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_destructor(self):
        self.generate_delete_destructor()

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject({copy_c_function}(other.{object_var}));'.format(
                copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix,
                object_var=Constants.object_var
            ))
        self.put_line('{class_name}(void *object_pointer, bool /*copy_constructor_from_raw*/)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject({copy_c_function}(object_pointer));'.format(
                copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix
            ))
        c_function_declaration = 'void* {copy_c_function}(void* object_pointer)'.format(
            copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix)
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('return new {0}(*static_cast<{0}*>(object_pointer));'.format(
                self.cur_class.m_implementation_class_name
            ))
        self.put_source_line('')


class RawPointerSemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_destructor(self):
        pass

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
        self.put_line('{class_name}(void *object_pointer, bool /*copy_constructor_from_raw*/)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject(object_pointer);')

    def generate_delete_method(self):
        self.put_line('void {0}()'.format(self.capi_generator.params_description.m_delete_method))
        with self.indent_scope():
            self.put_line('{delete_c_function}({object_var});'.format(
                delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix,
                object_var=Constants.object_var
            ))
            self.put_line('{object_var} = 0;'.format(object_var=Constants.object_var))
        c_function_declaration = 'void {delete_c_function}(void* object_pointer)'.format(
            delete_c_function=self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('delete static_cast<{0}*>(object_pointer);'.format(
                self.cur_class.m_implementation_class_name
            ))
        self.put_source_line('')


class RefCountedSemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_destructor(self):
        if not self.cur_class.m_base:
            self.put_line('~{class_name}()'.format(
                class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
            with self.indent_scope():
                self.put_line('{release_c_function}({object_var});'.format(
                    release_c_function=self.capi_generator.get_namespace_id().lower() + Constants.release_suffix,
                    object_var=Constants.object_var
                ))
            c_function_declaration = 'void {release_c_function}(void* object_pointer)'.format(
                release_c_function=self.capi_generator.get_namespace_id().lower() + Constants.release_suffix
            )
            self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
            with self.indent_scope_source():
                self.put_source_line('intrusive_ptr_release(static_cast<{0}*>(object_pointer));'.format(
                    self.cur_class.m_implementation_class_name
                ))
            self.put_source_line('')

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
            self.put_line('{addref_c_function}({object_var});'.format(
                addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.addref_suffix,
                object_var=Constants.object_var
            ))
        self.put_line('{class_name}(void *object_pointer, bool /*copy_constructor_from_raw*/)'.format(
            class_name=self.cur_class.m_name + self.capi_generator.params_description.m_wrapper_class_suffix))
        with self.indent_scope():
            self.put_line('SetObject(object_pointer);'.format(object_var=Constants.object_var))
            self.put_line('{addref_c_function}(object_pointer);'.format(
                addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.addref_suffix
            ))
        c_function_declaration = 'void {addref_c_function}(void* object_pointer)'.format(
            addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.addref_suffix
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('intrusive_ptr_add_ref(static_cast<{0}*>(object_pointer));'.format(
                self.cur_class.m_implementation_class_name
            ))
        self.put_source_line('')


str_to_lifecycle = {
    Parser.TLifecycle.copy_semantic: CopySemantic,
    Parser.TLifecycle.raw_pointer_semantic: RawPointerSemantic,
    Parser.TLifecycle.reference_counted: RefCountedSemantic
}


def create_lifecycle_traits(cur_class, capi_generator):
    if cur_class.m_lifecycle in str_to_lifecycle:
        return str_to_lifecycle[cur_class.m_lifecycle](cur_class, capi_generator)
    raise ValueError


class CreateLifecycleTraits(object):
    def __init__(self, cur_class, capi_generator):
        self.cur_class = cur_class
        self.capi_generator = capi_generator

    def __enter__(self):
        self.capi_generator.lifecycle_traits = create_lifecycle_traits(self.cur_class, self.capi_generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.capi_generator.lifecycle_traits
        self.capi_generator.lifecycle_traits = None
