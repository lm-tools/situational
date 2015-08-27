import inspect
import os
import types

import vcr

_CASSETTE_LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'cassettes')


def _cassette_path(function):
    module_path_part = inspect.getmodule(function).__name__.split(".")
    function_path_part = function.__qualname__.split(".")
    cassette_path = module_path_part + function_path_part
    return os.path.join(_CASSETTE_LIBRARY_PATH, *cassette_path)

_VCR = vcr.VCR(
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    func_path_generator=_cassette_path,
    filter_query_parameters=['app_key', 'app_id'],
)


class _VCROnAllTestsMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in iter(attrs.items()):
            if attr_name.startswith('test_') and \
                    isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = _VCR.use_cassette(attr_value)

        return super(_VCROnAllTestsMeta, cls).__new__(cls, name, bases, attrs)


class VCROnAllTests(metaclass=_VCROnAllTestsMeta):
    pass
