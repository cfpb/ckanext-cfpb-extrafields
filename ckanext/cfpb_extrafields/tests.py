import unittest

from nose_parameterized import parameterized
from nose.tools import assert_equal
import mock

import validators as v


class TestValidators(unittest.TestCase):
    @parameterized.expand(
        [(.1,), (.0001,), (1,), (1000000,), (9999.9999999,), ]
    )
    def test_positive_number_validator_valid(self, input):
        result = v.positive_number_validator(input)
        assert_equal(input, result)

    @parameterized.expand(
        [("a",), ("<script>alert('hi');</script>",), (-.01,), (-1,), (-1000000,), (-9999.9999999,), ]
    )
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_positive_number_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.positive_number_validator(input)


    @parameterized.expand([("5555-6666",), ("6666-4444",), ])
    def test_pra_control_num_validator_valid(self, input):
        assert_equal(input, v.pra_control_num_validator(input))

    @parameterized.expand([("a",), ("a666-4444",), ("7777-a888",), ("aaaa-bbbb",), ("77778888",), ])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_pra_control_num_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.pra_control_num_validator(input)