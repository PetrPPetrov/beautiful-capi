import Helpers
import Parser


def get_class_type(type_name: str, api_description: Parser.TBeautifulCapiRoot):
    path_to_class = type_name.split('::')
    return __get_class_type_impl(path_to_class, api_description.namespaces)


def __get_class_type_impl(path_to_class, classes_or_namespaces):
    for class_or_namespace in classes_or_namespaces:
        if class_or_namespace.name == path_to_class[0]:
            if len(path_to_class) == 1:
                return class_or_namespace
            elif len(path_to_class) == 2:
                return __get_class_type_impl(path_to_class[1:], class_or_namespace.classes)
            else:
                return __get_class_type_impl(path_to_class[1:], class_or_namespace.namespaces)
    return None


def get_c_type(type_name, api_description):
    return get_flat_type(type_name, api_description)


def get_flat_type(type_name, api_description):
    if not type_name:
        return 'void'
    if is_class_type(type_name, api_description):
        return 'void*'
    return type_name


def is_class_type(type_name, api_description):
    path_to_class = type_name.split('::')
    return __is_class_type_impl(path_to_class, api_description.namespaces)


def __is_class_type_impl(path_to_class, classes_or_namespaces):
    return bool(__get_class_type_impl(path_to_class, classes_or_namespaces))


def capi_down_cast(base_name, derived_name, namespaces):
    return  base_name.lower().replace('::', '_') + '_cast_to_' + '_'.join(namespaces).lower() + '_' + derived_name.lower()


def capi_function(name, namespaces):
    return ('_'.join(namespaces).lower() + '_' + Helpers.pascal_to_stl(name)).replace('__', '_')


def capi_method(name, namespaces):
    return '_'.join(list(namespaces) + [name]).lower()


def capi_destructor(clas: Parser.TClass, namespaces):
    class_name = '_'.join(list(namespaces) + [clas.name]).lower()
    if clas.lifecycle != Parser.TLifecycle.reference_counted:
        return class_name + '_delete'
    else:
        return class_name + '_release'


def capi_to_base(clas: Parser.TClass, namespaces):
    class_name = '_'.join(list(namespaces) + [clas.name]).lower()
    return class_name + '_cast_to_base'