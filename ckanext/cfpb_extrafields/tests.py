import unittest

from nose_parameterized import parameterized
from nose.tools import assert_equal
import mock

import validators as v


class TestValidators(unittest.TestCase):
    
    @parameterized.expand([
        (u'"asdf","asdf,asdf"',[u'asdf', u'asdf,asdf']),
        (u'asdf',[u'asdf']),
        (u'a',[u'a']),
        (u'{"blah blah","blah asdf",asdf}',[u'blah blah', u'blah asdf', u'asdf']),
        (u'{asdf,asdf}',[u'asdf', u'asdf']),
        (u'{"asdf,asdf",asdf}',[u'asdf,asdf', u'asdf']),
        (u'{"asdf,asdf","asdf asdf"}',[u'asdf,asdf',u'asdf asdf']),
        (u'{asdf,"asdf asdf"}',[u'asdf', u'asdf asdf']),
        (u'{a,"f d",d}',[u'a', u'f d', u'd']),
    ]) 
    def test_clean_select_multi(self, ms, expected):
        print ms
        print expected
        assert_equal(v.clean_select_multi(ms), expected)
    
    @parameterized.expand([("note0 note1",), ("http://www.~/hi",), ])
    def test_input_value_validator(self, input):
        assert_equal(input, v.input_value_validator(input))
    @parameterized.expand([("__Other",), ])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_input_value_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.input_value_validator(input)

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

    @parameterized.expand([("DI66666",), ("DI00001",), ])
    def test_dig_id_validator(self, input):
        assert_equal(input, v.dig_id_validator(input))
    @parameterized.expand([("a",), ("64444",), ("DI7777",), ("DI-12345",), ("DI1234",), ])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_dig_id_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.dig_id_validator(input)

    @parameterized.expand([("2010-10-01",), ("1995-01-01",), ("2100-10-20",), (None,), ])
    def test_reasonable_date_validator(self, input):
        assert_equal(input, v.reasonable_date_validator(input))
    @parameterized.expand([("a",), ("1500-01-01",), ("27901-01-01",), ("2012/12/21",), ("2012/1/1",), ("2012-21-01",), ("2012-10-a1",), ]) #, ("2012-10-1",)
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_reasonable_date_validator(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.reasonable_date_validator(input)

    @parameterized.expand([("5555-6666",), ("6666-4444",), ])
    def test_pra_control_num_validator_valid(self, input):
        assert_equal(input, v.pra_control_num_validator(input))
    @parameterized.expand([("a",), ("a666-4444",), ("7777-a888",), ("aaaa-bbbb",), ("77778888",), ])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_pra_control_num_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.pra_control_num_validator(input)
