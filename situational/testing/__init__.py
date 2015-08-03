from django.test import TestCase

from .vcr_on_all_tests import VCROnAllTests


class BaseCase(TestCase, VCROnAllTests):
    pass
