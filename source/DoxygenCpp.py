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

from FileGenerator import FileGenerator
from DocumentationGenerator import ReferenceGenerator
from Parser import TGenericDocumentation, TDocumentation, TEnumeration, TNamespace


class DoxygenCppGenerator(object):
    @staticmethod
    def __add_line(result_lines: [], line: str, need_eol: bool):
        if line is not None:
            if need_eol or not result_lines:
                result_lines.append(line)
            else:
                result_lines[-1] += ' ' + line

    @staticmethod
    def __get_lines_for_generic_documentation(doc: TGenericDocumentation) -> [str]:
        result_lines = []
        need_eol = True
        for doc_item in doc.all_items:
            if type(doc_item) is str:
                DoxygenCppGenerator.__add_line(result_lines, doc_item, need_eol)
                need_eol = True
            elif type(doc_item) is ReferenceGenerator:
                need_eol = False
                text = doc_item.text.strip()
                if text:
                    reference_as_text = '@ref ' + text
                    DoxygenCppGenerator.__add_line(result_lines, reference_as_text, need_eol)
            elif doc_item in doc.references:
                need_eol = False
                reference_as_text = '@ref ' + ' '.join(doc_item.all_items)
                DoxygenCppGenerator.__add_line(result_lines, reference_as_text, need_eol)
            elif doc_item in doc.see_alsos:
                need_eol = True
                see_also = '@see '
                DoxygenCppGenerator.__add_line(result_lines, see_also, need_eol)
                need_eol = False
                for new_doc_item in DoxygenCppGenerator.__get_lines_for_generic_documentation(doc_item):
                    DoxygenCppGenerator.__add_line(result_lines, new_doc_item, need_eol)
                    need_eol = True
                need_eol = False
        return result_lines

    @staticmethod
    def __get_lines_for_documentation(some_doc, generate_doc_return: bool) -> [str]:
        result_lines = []
        if issubclass(type(some_doc), TDocumentation):
            for brief in some_doc.briefs:
                for brief_line in DoxygenCppGenerator.__get_lines_for_generic_documentation(brief):
                    brief_text = brief_line.strip()
                    if brief_text:
                        result_lines.append('@brief {0}'.format(brief_text))
            if generate_doc_return:
                for returns in some_doc.returns:
                    for return_line in DoxygenCppGenerator.__get_lines_for_generic_documentation(returns):
                        return_text = return_line.strip()
                        if return_text:
                            result_lines.append('@returns {0}'.format(return_text))
        for generic_line in DoxygenCppGenerator.__get_lines_for_generic_documentation(some_doc):
            result_lines.append(generic_line)
        return result_lines

    @staticmethod
    def generate_for_class(out: FileGenerator, class_generator):
        if class_generator.class_object.documentations and not class_generator.is_template:
            out.put_line('/**')
            docs = []
            if class_generator.params.doxygen_class_pattern:
                docs.append(class_generator.params.doxygen_class_pattern)
            for documentation in class_generator.class_object.documentations:
                docs += DoxygenCppGenerator.__get_lines_for_documentation(documentation, False)
            for doc_line in docs:
                out.put_line(' * {0}'.format(doc_line.format(
                    file=class_generator.file_cache.class_header(class_generator.full_name_array),
                    file_decl=class_generator.file_cache.class_header_decl(class_generator.full_name_array),
                    wrap_name=class_generator.wrap_name
                )))
            out.put_line(' */')

    @staticmethod
    def generate_for_template(out: FileGenerator, template_generator):
        class_ = template_generator.template_object.classes[0]
        template_types = []
        for template_argument in template_generator.template_object.arguments:
            if template_argument.type_name in ['template', 'class', 'typename']:
                template_types.append(template_argument.name)
        if class_.documentations:
            out.put_line('/**')
            out.put_line(' * @ingroup {0}'.format('_'.join(template_generator.parent_namespace.full_name_array)))
            out.put_line(' * @class {0}'.format(template_generator.template_class_generator.wrap_name))
            for documentation in class_.documentations:
                for doc_line in DoxygenCppGenerator.__get_lines_for_documentation(documentation, True):
                    out.put_line(' * {0}'.format(doc_line))
            for argument in template_generator.template_object.arguments:
                for documentation in argument.documentations:
                    doc_lines = DoxygenCppGenerator.__get_lines_for_documentation(documentation, True)
                    if argument.type_name in template_types:
                        out.put_line(' * @tparam {0} {1}'.format(argument.name, ''.join(doc_lines)))
                    else:
                        out.put_line(' * @param {0} {1}'.format(argument.name, ''.join(doc_lines)))
            out.put_line(' */')

    @staticmethod
    def generate_for_template_method(out: FileGenerator, template_generator, method_generator):
        template_types = []
        for template_argument in template_generator.template_object.arguments:
            if template_argument.type_name in ['template', 'class', 'typename']:
                template_types.append(template_argument.name)
        if method_generator.method_object.documentations:
            out.put_line('/**')
            for documentation in method_generator.method_object.documentations:
                for doc_line in DoxygenCppGenerator.__get_lines_for_documentation(documentation, True):
                    out.put_line(' * {0}'.format(doc_line))
            for argument in method_generator.method_object.arguments:
                for documentation in argument.documentations:
                    doc_lines = DoxygenCppGenerator.__get_lines_for_documentation(documentation, True)
                    if argument.type_name in template_types:
                        out.put_line(' * @tparam {0} {1}'.format(argument.name, ''.join(doc_lines)))
                    else:
                        out.put_line(' * @param {0} {1}'.format(argument.name, ''.join(doc_lines)))
            out.put_line(' */')
        
    @staticmethod
    def generate_for_namespace(out: FileGenerator, namespace_object: TNamespace, full_wrap_name: str):
        if namespace_object.documentations:
            out.put_line('/**')
            out.put_line(' * @namespace ' + full_wrap_name)
            for documentation in namespace_object.documentations:
                for doc_line in DoxygenCppGenerator.__get_lines_for_documentation(documentation, False):
                    out.put_line(' * {0}'.format(doc_line))
            out.put_line(' */')

    @staticmethod
    def generate_for_enum(out: FileGenerator, enum_object: TEnumeration):
        if enum_object.documentations:
            out.put_line('/**')
            for documentation in enum_object.documentations:
                for doc_line in DoxygenCppGenerator.__get_lines_for_documentation(documentation, False):
                    out.put_line(' * {0}'.format(doc_line))
            out.put_line(' */')

    @staticmethod
    def get_for_enum_item(enum_item) -> str:
        result = []
        for documentation in enum_item.documentations:
            result += DoxygenCppGenerator.__get_lines_for_documentation(documentation, False)
        result_str = ''.join(result)
        return ' /**< {0} */'.format(result_str) if result_str else ''

    @staticmethod
    def generate_for_routine(out: FileGenerator, routine_object, generator):
        if routine_object.documentations:
            out.put_line('/**')
            for documentation in routine_object.documentations:
                for doc_line in DoxygenCppGenerator.__get_lines_for_documentation(documentation, True):
                    out.put_line(' * {0}'.format(doc_line))
            for argument_generator in generator.argument_generators:
                for documentation in argument_generator.argument_object.documentations:
                    doc_lines = DoxygenCppGenerator.__get_lines_for_documentation(documentation, True)
                    out.put_line(' * @param {0} {1}'.format(argument_generator.name, ''.join(doc_lines)))
            out.put_line(' */')
