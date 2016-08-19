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

import argparse
import os

import ParamsParser
import Parser
import TypeInfo
from FileGenerator import FileGenerator, IndentScope


def to_cs_name(type_name: str):
    return type_name.replace('::', '.')


def get_cs_capi_pass_type(type_name: str, api_description: Parser.TBeautifulCapiRoot):
    c_type = TypeInfo.get_c_type(type_name, api_description)

    cs_type = c_type
    if c_type == 'void*':
        cs_type = 'global::System.IntPtr'

    if TypeInfo.is_class_type(type_name, api_description):
        cs_type = 'global::System.Runtime.InteropServices.HandleRef'

    if c_type == 'const char*':
        cs_type = 'string'

    if c_type == 'size_t':
        cs_type = 'global::System.UIntPtr'

    if c_type == 'int8_t':
        cs_type = 'sbyte'

    if c_type == 'unsigned char' or c_type == 'uint8_t':
        cs_type = 'byte'

    if c_type == 'short' or c_type == 'int16_t':
        cs_type = 'sbyte'

    if c_type == 'unsigned short' or c_type == 'uint16_t':
        cs_type = 'byte'

    if c_type == 'int' or c_type == 'int32_t':
        cs_type = 'int'

    if c_type == 'unsigned int' or c_type == 'uint32_t':
        cs_type = 'uint'

    if c_type == 'long' or c_type == 'int64_t':
        cs_type = 'long'

    if c_type == 'unsigned long' or c_type == 'uint64_t':
        cs_type = 'ulong'

    return cs_type


def get_cs_capi_ret_type(type_name: str, api_description: Parser.TBeautifulCapiRoot):
    c_type = TypeInfo.get_c_type(type_name, api_description)

    cs_type = c_type
    if c_type == 'void*' or c_type == 'const char*' or TypeInfo.is_class_type(type_name, api_description):
        cs_type = 'global::System.IntPtr'

    if c_type == 'size_t':
        cs_type = 'global::System.UIntPtr'

    if c_type == 'int8_t':
        cs_type = 'sbyte'

    if c_type == 'unsigned char' or c_type == 'uint8_t':
        cs_type = 'byte'

    if c_type == 'short' or c_type == 'int16_t':
        cs_type = 'sbyte'

    if c_type == 'unsigned short' or c_type == 'uint16_t':
        cs_type = 'byte'

    if c_type == 'int' or c_type == 'int32_t':
        cs_type = 'int'

    if c_type == 'unsigned int' or c_type == 'uint32_t':
        cs_type = 'uint'

    if c_type == 'long' or c_type == 'int64_t':
        cs_type = 'long'

    if c_type == 'unsigned long' or c_type == 'uint64_t':
        cs_type = 'ulong'

    return cs_type


def get_cs_type(type_name: str, api_description: Parser.TBeautifulCapiRoot):
    cs_type = to_cs_name(type_name)

    if cs_type == 'void*':
        cs_type = 'global::System.IntPtr'

    if cs_type == 'const char*':
        cs_type = 'string'

    if TypeInfo.is_class_type(type_name, api_description):
        cs_type = 'global::' + cs_type

    if cs_type == 'size_t':
        cs_type = 'ulong'

    if cs_type == 'int8_t':
        cs_type = 'sbyte'

    if cs_type == 'unsigned char' or cs_type == 'uint8_t':
        cs_type = 'byte'

    if cs_type == 'short' or cs_type == 'int16_t':
        cs_type = 'sbyte'

    if cs_type == 'unsigned short' or cs_type == 'uint16_t':
        cs_type = 'byte'

    if cs_type == 'int' or cs_type == 'int32_t':
        cs_type = 'int'

    if cs_type == 'unsigned int' or cs_type == 'uint32_t':
        cs_type = 'uint'

    if cs_type == 'long' or cs_type == 'int64_t':
        cs_type = 'long'

    if cs_type == 'unsigned long' or cs_type == 'uint64_t':
        cs_type = 'ulong'

    return cs_type


class Argument(object):
    def __init__(self, api_description: Parser.TBeautifulCapiRoot, name: str, type_name='void'):
        self.name = name
        self.type_name = type_name
        self.api = api_description

    @property
    def is_class(self):
        return TypeInfo.is_class_type(self.type_name, self.api)

    def type_pass_to_c(self):
        return get_cs_capi_pass_type(self.type_name, self.api)

    def type_pass_to_cs(self):
        return get_cs_type(self.type_name, self.api)

    def type_return_from_c(self):
        return get_cs_capi_ret_type(self.type_name, self.api)

    def type_return_from_cs(self):
        return get_cs_type(self.type_name, self.api)

    def value_pass_to_c(self):
        if self.is_class:
            res = '{cs_type}.getCPtr({name})'.format(name=self.name, cs_type=self.type_pass_to_cs())
        elif self.type_name == 'size_t':
            res = '({c_type}){name}'.format(name=self.name, c_type=self.type_pass_to_c())
        else:
            res = self.name
        return res


class Description(object):
    def __init__(self, input_xml: str, input_params: str):
        self.capi_name = os.path.splitext(os.path.basename(input_xml))[0]

        from xml.dom.minidom import parse
        self.params = ParamsParser.load(parse(input_params))
        self.api = Parser.load(parse(input_xml))


class FileCreator(object):
    def __init__(self):
        self.file = None
        self.additional_format = {}

    def create_file(self, folder: str, name: str, params: ParamsParser.TBeautifulCapiParams):
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.file = FileGenerator(os.path.join(folder, name))
        self.file.copyright_header = params.copyright_header
        self.file.automatic_generation_warning = params.automatic_generated_warning

    @property
    def format_args(self):
        return {self.__class__.__name__.lower(): self}

    def write(self, text: str or list, **kwargs):
        if isinstance(text, str):
            self.__write_line(text, **kwargs)
        elif isinstance(text, list):
            for line in text:
                self.__write_line(line, **kwargs)

    def __write_line(self, line: str, **kwargs):
        if self.file:
            written = line.strip()
            do_format = written not in '{}'

            self.file.put_line(written.format(**self.format_args, **self.additional_format, **kwargs) if do_format else written)

    def scope(self):
        return IndentScope(self.file)

    def add_format(self, **kwargs):
        return FormatArgs(self, **kwargs)


class FormatArgs(object):
    def __init__(self, file_creator: FileCreator, **kwargs):
        self.file_creator = file_creator
        self.new_additional = kwargs
        self.old_additional = file_creator.additional_format

    def __enter__(self):
        additional = dict()
        additional.update(self.old_additional)
        additional.update(self.new_additional)
        self.file_creator.additional_format = additional

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_creator.additional_format = self.old_additional


class Module(FileCreator):
    def __init__(self, name: str, description: Description, root_folder: str):
        super().__init__()
        self.name = name
        self.description = description
        self.root_folder = root_folder

    @property
    def api(self):
        return self.description.api

    @property
    def module_c_name(self):
        return self.description.capi_name

    @property
    def invoke_module(self):
        return self.name + 'PINVOKE'

    def generate(self):
        self.create_file(self.root_folder, self.invoke_module + '.cs', self.description.params)

        self.write('class {module.invoke_module}')
        with self.scope():
            for namespace in self.api.namespaces:
                Namespace(namespace, self, self.root_folder).generate()

    def generate_function_invoke(self, function, name: str, args=list()):
        self.__generate_function_invoke(function, name, args, 'global::System.IntPtr')

    def generate_method_invoke(self, function, name: str):
        self.__generate_function_invoke(function, name, list(), 'void')

    def __generate_function_invoke(self, function, name: str, additional_args, default_return: str):
        args = additional_args
        if function:
            args += function.arguments_c

        return_type = Argument(self.api, 'ret',
                               function.function.return_type if function.function and hasattr(function.function,'return_type') else default_return)

        self.generate_invoke(name, return_type, args)

    def generate_invoke(self, name: str, return_type: Argument, args: list):
        self.generate_import_attribute(name)
        self.generate_import_declaration(args, name, return_type)
        self.write('')

    def generate_import_attribute(self, name: str):
        self.write(
            '[global::System.Runtime.InteropServices.DllImport("{module.module_c_name}", EntryPoint="{capi_function}")]',
            capi_function=name
            )

    def generate_import_declaration(self, args: list, name: str, return_type: Argument):
        self.write(
            'public static extern {ret_type} {invoke_function}({args});',
            capi_function=name,
            invoke_function=self.invoke_name(name),
            ret_type=return_type.type_return_from_c(),
            args=', '.join([arg.type_pass_to_c() + ' ' + arg.name for arg in args])
        )

    @staticmethod
    def invoke_name(c_name: str):
        return 'Invoke_' + c_name


class Namespace(FileCreator):
    def __init__(self, namespace: Parser.TNamespace, module: Module, root_folder: str):
        super().__init__()
        self.namespace = namespace
        self.module = module
        self.root_folder = root_folder
        self.namespace_path = list(os.path.split(os.path.relpath(os.path.join(root_folder, namespace.name), self.module.root_folder)))
        if self.namespace_path[0] == '':
            self.namespace_path = self.namespace_path[1:]

    @property
    def format_args(self):
        args = super().format_args
        args.update({'module': self.module})
        return args

    @property
    def name(self):
        return self.namespace.name

    @property
    def path(self):
        return '.'.join(self.namespace_path)

    @property
    def containing_namespace(self):
        return '.'.join(self.namespace_path[:-1])

    def generate(self):
        self.create_file(self.root_folder, self.name + '.cs', self.module.description.params)

        if len(self.namespace_path) > 1:
            self.write('namespace {namespace.containing_namespace}')
            with self.scope():
                self.generate_ns_class()
        else:
            self.generate_ns_class()

    def generate_ns_class(self):
        self.write('public class {namespace.name}NS')
        with self.scope():
            for function in self.namespace.functions:
                Function(function, self).generate()

            for clas in self.namespace.classes:
                Class(clas, self, os.path.join(self.root_folder, self.name)).generate()

            for namespace in self.namespace.namespaces:
                Namespace(namespace, self.module, os.path.join(self.root_folder, self.name)).generate()


class Class(FileCreator):
    def __init__(self, clas: Parser.TClass, namespace: Namespace, root_folder: str):
        super().__init__()
        self.namespace = namespace
        self.clas = clas
        self.root_folder = root_folder

    @property
    def format_args(self):
        args = super().format_args
        args.update({'namespace': self.namespace, 'module': self.module})
        return args

    @property
    def name(self):
        return self.clas.name

    @property
    def type_name(self):
        return self.namespace.path + '::' + self.clas.name

    @property
    def has_base(self):
        return self.clas.base_filled and self.clas.base

    @property
    def capi_destructor(self):
        return TypeInfo.capi_destructor(self.clas, self.namespace.namespace_path)

    @property
    def invoke_destructor(self):
        return self.module.invoke_name(self.capi_destructor)

    @property
    def virtual_attribute(self):
        return 'override' if self.has_base else 'virtual'

    @property
    def module(self):
        return self.namespace.module

    @property
    def api(self):
        return self.module.api

    def generate(self):
        self.create_file(self.root_folder, self.name + '.cs', self.module.description.params)

        self.write('namespace {namespace.path}')
        with self.scope():
            bases = ['global::System.IDisposable']
            if self.has_base:
                bases = [to_cs_name(self.clas.base)]

            self.write('public class {class.name} : {bases}', bases=', '.join(bases))

            with self.scope():
                self.generate_fields()
                self.generate_internal_constructor()
                self.generate_c_ptr_getter()
                self.generate_destructor()

                for ctor in self.clas.constructors:
                    Constructor(ctor, self).generate()

                for method in self.clas.methods:
                    Method(method, self).generate()

        self.generate_casts()

    def generate_destructor(self):
        self.module.generate_invoke(
            return_type=Argument(self.api, 'ret'),
            name=self.capi_destructor,
            args=[Argument(self.api, 'class_arg', self.type_name)])

        self.write('~{class.name}()')
        with self.scope():
            self.write('Dispose();')
        self.write('')
        self.write('public {class.virtual_attribute} void Dispose()')
        with self.scope():
            self.write('lock(this)')
            with self.scope():
                self.write('if (capi_ptr.Handle != global::System.IntPtr.Zero)')
                with self.scope():
                    self.write('if (capi_owned)')
                    with self.scope():
                        self.write('capi_owned = false;')
                        self.write('{module.invoke_module}.{class.invoke_destructor}(capi_ptr);')
                    self.write('capi_ptr = new global::System.Runtime.InteropServices.HandleRef(null, global::System.IntPtr.Zero);')
                self.write('global::System.GC.SuppressFinalize(this);')
                if self.has_base:
                    self.write('base.Dispose();')

    def generate_c_ptr_getter(self):
        self.write('internal static global::System.Runtime.InteropServices.HandleRef getCPtr({class.name} obj)')
        with self.scope():
            self.write(
                'return (obj == null) ? new global::System.Runtime.InteropServices.HandleRef(null, global::System.IntPtr.Zero) : obj.capi_ptr;')
        self.write('')

    def generate_internal_constructor(self):
        if self.has_base:
            self.write(
                'internal {class.name}(global::System.IntPtr c_ptr, bool owned) : base({module.invoke_module}.{invoke_base}(c_ptr), owned)',
                invoke_base=self.module.invoke_name(TypeInfo.capi_to_base(self.clas, self.namespace.namespace_path)))
        else:
            self.write('internal {class.name}(global::System.IntPtr c_ptr, bool owned)')
        with self.scope():
            if not self.has_base:
                self.write('capi_owned = owned;')
            self.write('capi_ptr = new global::System.Runtime.InteropServices.HandleRef(this, c_ptr);')
        self.write('')

    def generate_fields(self):
        self.write('private global::System.Runtime.InteropServices.HandleRef capi_ptr;')
        if not self.has_base:
            self.write('protected bool capi_owned;')
        self.write('')

    def generate_casts(self):
        if not self.clas.base_filled:
            return

        base_type = TypeInfo.get_class_type(self.clas.base, self.api)
        base_name = self.clas.base

        self.module.generate_invoke(
            return_type=Argument(self.api, 'ret', base_name),
            name=TypeInfo.capi_method('cast_to_base', self.namespace.namespace_path + [self.name]),
            args=[Argument(self.api, 'class_ptr', 'global::System.IntPtr')])

        while base_type:
            capi_cast_name = TypeInfo.capi_down_cast(base_name, self.name, self.namespace.namespace_path)

            self.module.generate_invoke(
                return_type=Argument(self.api, 'ret', self.type_name),
                name=capi_cast_name,
                args=[Argument(self.api, 'class_arg', base_name)])

            with self.namespace.add_format(
                    derived=to_cs_name(self.type_name),
                    cast_name=base_type.name + '_to_' + self.name,
                    invoke_cast_name=self.module.invoke_name(capi_cast_name),
                    base=to_cs_name(base_name)):
                self.namespace.write('')
                self.namespace.write('public static {derived} {cast_name}({base} base_ptr)')
                with self.namespace.scope():
                    self.namespace.write('global::System.IntPtr c_ptr = {module.invoke_module}.{invoke_cast_name}({base}.getCPtr(base_ptr));')
                    self.namespace.write('{derived} ret = (c_ptr == global::System.IntPtr.Zero) ? null : new {derived}(c_ptr, false);')
                    self.namespace.write('return ret;')

            base_name = base_type.base
            base_type = TypeInfo.get_class_type(base_type.base, self.api)


class FunctionBase(object):
    def __init__(self,
                 function: Parser.TConstructor or Parser.TMethod or Parser.TFunction,
                 container: Class or Namespace):
        self.function = function
        self.container = container

    @property
    def module(self):
        return None

    @property
    def namespace_path(self):
        return None

    @property
    def capi_name(self):
        return None

    @property
    def return_type(self):
        return Argument(self.module.api, 'ret', self.function.return_type if self.function.return_type else 'void')

    @property
    def arguments_c(self):
        return self.arguments_cs

    @property
    def arguments_cs(self):
        return [Argument(self.module.api, arg.name, arg.type_name) for arg in self.function.arguments]

    @staticmethod
    def arguments_pass(arguments):
        arg_names = [arg.value_pass_to_c() for arg in arguments]
        return arg_names

    @staticmethod
    def arguments_description(arguments):
        return [arg.type_pass_to_cs() + ' ' + arg.name for arg in arguments]

    def generate_invoke(self):
        self.module.generate_function_invoke(self, self.capi_name, list())

    @property
    def attr(self):
        return ''

    def generate(self):
        self.generate_invoke()

        with self.container.add_format(
                cs_attr=self.attr,
                ret_type=self.return_type.type_pass_to_cs(),
                cs_name=self.function.name,
                invoke_name=self.module.invoke_name(self.capi_name),
                cs_args=', '.join(self.arguments_description(self.arguments_cs)),
                c_args=', '.join(self.arguments_pass(self.arguments_c))):

            self.container.write('')
            self.container.write('public {cs_attr} {ret_type} {cs_name}({cs_args})')

            with self.container.scope():
                call = '{module.invoke_module}.{invoke_name}({c_args})'

                if TypeInfo.is_class_type(self.function.return_type, self.module.description.api):
                    self.container.write('global::System.IntPtr c_ptr = {call};'.format(call=call))
                    self.container.write('{ret_type} ret = (c_ptr == global::System.IntPtr.Zero) ? null : new {ret_type}(c_ptr, false);')
                    self.container.write('return ret;')
                elif self.return_type.type_pass_to_cs() == 'string':
                    self.container.write('global::System.IntPtr c_ptr = {call};'.format(call=call))
                    self.container.write('global::System.String ret = (c_ptr == global::System.IntPtr.Zero) ? null : global::System.Runtime.InteropServices.Marshal.PtrToStringAuto(c_ptr);')
                    self.container.write('return ret;')
                elif self.return_type.type_name == 'size_t':
                    self.container.write('return ({cs_type}){call};'.format(call=call, cs_type=self.return_type.type_pass_to_cs()))
                else:
                    line = call + ';'
                    if self.function.return_type and self.function.return_type != 'void':
                        line = 'return ' + line
                    self.container.write(line)


class Function(FunctionBase):
    def __init__(self, function: Parser.TFunction, namespace: Namespace):
        super().__init__(function, namespace)

    @property
    def module(self):
        return self.container.module

    @property
    def namespace_path(self):
        return self.container.namespace_path

    @property
    def capi_name(self):
        return TypeInfo.capi_function(self.function.name, self.namespace_path)

    @property
    def attr(self):
        return 'static'


class Method(FunctionBase):
    def __init__(self, method: Parser.TMethod or Parser.TConstructor, clas: Class):
        super().__init__(method, clas)

    @property
    def module(self):
        return self.container.namespace.module

    @property
    def capi_name(self):
        return TypeInfo.capi_method(self.function.name, self.namespace_path)

    @property
    def namespace_path(self):
        return tuple(list(self.container.namespace.namespace_path) + [self.container.clas.name])

    @property
    def arguments_c(self):
        return [Argument(self.module.api, 'capi_ptr', 'global::System.Runtime.InteropServices.HandleRef')] + self.arguments_cs

    def generate_invoke(self):
        self.module.generate_method_invoke(self, self.capi_name)


class Constructor(Method):
    def __init__(self, constructor: Parser.TConstructor, clas: Class):
        super().__init__(constructor, clas)

    @property
    def capi_name(self):
        return TypeInfo.capi_function(self.function.name, self.namespace_path)

    @property
    def arguments_c(self):
        return super(Method, self).arguments_c

    def generate(self):
        self.generate_invoke()

        self.container.write('')
        self.container.write(
            'public {name}({arg_desc}) : this({module.invoke_module}.{invoke_ctor}({arg_names}), true)',
            name=self.container.name,
            invoke_ctor=self.module.invoke_name(self.capi_name),
            arg_desc=', '.join(self.arguments_description(self.arguments_cs)),
            arg_names=', '.join(self.arguments_pass(self.arguments_c)))

        with self.container.scope():
            pass

    def generate_invoke(self):
        return super(Method, self).generate_invoke()


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi Swig',
        description='This program generates Swig wrappers for your C++ classes.')

    parser.add_argument(
        '-i', '--input', nargs=None, default='input.xml', metavar='INPUT',
        help='specifies input API description file')
    parser.add_argument(
        '-p', '--params', nargs=None, default='params.xml', metavar='PARAMS',
        help='specifies wrapper generation parameters input file')
    parser.add_argument(
        '-o', '--output-folder', nargs=None, default='./output', metavar='OUTPUT_FOLDER',
        help='specifies output folder for generated files')
    parser.add_argument(
        '-m', '--module-name', nargs=None, default='', metavar='MODULE_NAME',
        help='specifies module name for wrapper')

    args = parser.parse_args()

    description = Description(os.path.expandvars(args.input), os.path.expandvars(args.params))
    module = Module(os.path.expandvars(args.module_name), description, os.path.expandvars(args.output_folder))
    module.generate()

main()
