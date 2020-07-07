import unittest
import datetime as dt

from nose_parameterized import parameterized
from nose.tools import assert_equal
import mock

import validators as v
import ckanext.cfpb_extrafields.exportutils as eu
import ckanext.cfpb_extrafields.digutils as du

# Show diffs even when they're large
assert_equal.__self__.maxDiff = None

class TestValidators(unittest.TestCase):
    maxDiff=None
    @parameterized.expand([
        #(u'"asdf","asdf,asdf"',[u'asdf', u'asdf,asdf']),
        (u'"asdf","asdf,asdf"',[u'"asdf","asdf,asdf"']),
        (u'asdf',[u'asdf']),
        (u'asdf, asdf',[u'asdf, asdf']),
        (u'a',[u'a']),
        (u'{"blah blah","blah asdf",asdf}',[u'blah blah', u'blah asdf', u'asdf']),
        (u'{asdf,asdf}',[u'asdf', u'asdf']),
        (u'{"asdf,asdf",asdf}',[u'asdf,asdf', u'asdf']),
        (u'{"asdf,asdf","asdf asdf"}',[u'asdf,asdf',u'asdf asdf']),
        (u'{asdf,"asdf asdf"}',[u'asdf', u'asdf asdf']),
        (u'{a,"f d",d}',[u'a', u'f d', u'd']),
        (u'',[]),
        (["foo"],["foo"]),
        (u'''{123Consumers,123-Consumers,"123,Consumers",123.Consumers,123?Consumers,123<>Consumers,"123{}Consumers",123[]Consumers,123()Consumers,"123\\Consumers",123+Consumers,123'Consumers}''',
        [
            u'123Consumers',
            u'123-Consumers',
            u"123,Consumers",
            u'123.Consumers',
            u'123?Consumers',
            u'123<>Consumers',
            u"123{}Consumers",
            u'123[]Consumers',
            u'123()Consumers',
            u"123\\Consumers",
            u'123+Consumers',
            u"123'Consumers"]
            ),
    ])
    def test_clean_select_multi(self, ms, expected):
        assert_equal(v.clean_select_multi(ms), expected)

        
    @parameterized.expand([("note0 note1",), ("http://www.~/hi",)])
    def test_input_value_validator(self, input):
        assert_equal(input, v.input_value_validator(input))
        
    @parameterized.expand([(["a", "a", "b"], ["a", "b"])])
    def test_input_value_validator_list(self, input, expected):
        assert_equal(expected, v.input_value_validator(input))

    @parameterized.expand([("__Other",), ("invalid<",), (">",)])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_input_value_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.input_value_validator(input)

            
    @parameterized.expand([(.1,), (.0001,), (1,), (1000000,), (9999.9999999,), ])
    def test_positive_number_validator_valid(self, input):
        result = v.positive_number_validator(input)
        assert_equal(input, result)
        
    @parameterized.expand([("a",), ("<script>alert('hi');</script>",),
                           (-.01,), (-1,), (-1000000,), (-9999.9999999,), ])
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

    @parameterized.expand([("2010-10-01", dt.datetime(2010, 10, 1)), (None, None), ("", None), ])
    def test_to_datetime(self, input, expected):
        assert_equal(v.to_datetime(input), expected)

    @parameterized.expand([("",), (None,)])
    def test_reasonable_date_validator_empty(self, input):
        self.assertIsNone(v.reasonable_date_validator(input))


    @parameterized.expand([("a",), ("1500-01-01",), ("27901-01-01",),
                           ("2012/12/21",), ("2012/1/1",), ("2012-21-01",),
                           ("2012-10-a1",)]) 
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_reasonable_date_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.reasonable_date_validator(input)

    @parameterized.expand([("2000-01-01", "2010-01-01"), ("2000-01-01", None)])
    def test_end_after_start_validator_valid(self, start, end):
        self.assertIsNone(v.end_after_start_validator(
            None,
            {
                "content_temporal_range_start": start,
                "content_temporal_range_end": end,
            },
            None,
            None,
        ))

    @parameterized.expand([("2010-01-01", "2000-01-01")])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_end_after_start_validator_invalid(self, start, end, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            self.assertIsNone(v.end_after_start_validator(
                None,
                {
                    ("content_temporal_range_start",): start,
                    ("content_temporal_range_end",): end,
                },
                None,
                None,
            ))

    @parameterized.expand([("5555-6666",), ("6666-4444",), ])
    def test_pra_control_num_validator_valid(self, input):
        assert_equal(input, v.pra_control_num_validator(input))
        
    @parameterized.expand([("a",), ("a666-4444",), ("7777-a888",), ("aaaa-bbbb",), ("77778888",), ])
    @mock.patch("ckanext.cfpb_extrafields.validators.Invalid")
    def test_pra_control_num_validator_invalid(self, input, mi):
        mi.side_effect = Exception("")
        with self.assertRaises(Exception):
            v.pra_control_num_validator(input)

    @parameterized.expand([
        ({}, {"db_roles": []}),
        (
            {"db_role_level_1": "role1", "db_role_level_3": "role_3", "db_desc_level_3": "desc3"},
            {"db_roles": [["role1", ""], ["role_3", "desc3"], ]}
        ),
    ])
    def test_combine_roles(self, data, expected):
        assert_equal(v.combine_roles(data), expected)

class TestExport(unittest.TestCase):
    @parameterized.expand([
        ({"a": {"str": "x"}}, {"a.str": "x"}),
        ({"a": {"int": 1}}, {"a.int": 1}),
        ({"a": {"list_str": ["x", "y", "z"]}}, {"a.list_str": "x,y,z"}),
        ({"a": {"list_dict": [{"x": "y"}, {}]}}, {"a.list_dict": '[{"x": "y"}, {}]'}),
    ])
    def test_flatten(self, data, expected):
        result = eu.flatten(data)
        assert_equal(result, expected)

    @parameterized.expand([
        ({}, {"a.list_str": "x,y,z"}),
        ({"list_sep": "; "}, {"a.list_str": "x; y; z"}),
        ({"list_sep": None}, {"a.list_str": '["x", "y", "z"]'}),
    ])
    def test_flatten_listseps(self, kwargs, expected):
        data = {"a": {"list_str": ["x", "y", "z"]}}
        result = eu.flatten(data, **kwargs)
        assert_equal(result, expected)
    
    @parameterized.expand([
        ([{"a":1, "b": 2, "c": 3}], ["b", "a"], {"a": "A", "b": "bee"}, "bee,A\r\n2,1\r\n"),
    ])
    def test_to_csv(self, data, fields, fieldmap, expected):
        result = eu.to_csv(data, fields, fieldmap)
        assert_equal(result, expected)

class MockCell(object):
    def __init__(self, val):
        self.value = val

class TestImport(unittest.TestCase):
    @parameterized.expand([
        ("s", "s"),
        ("", ""),
        (1, ""),
        (dt.datetime.now(), ""),
    ])
    def test_strfy(self, data, expected):
        result = du.strfy(data)
        assert_equal(result, expected)

    def test_concat(self):
        sheet = {
            "A39": MockCell("foo"),
            "B39": MockCell("bar"),
            "C39": MockCell("baz"),
        }
        result = du.concat(["A39", "B39", "C39"])(sheet)
        assert_equal(result, "foobarbaz")

    @parameterized.expand([
        ("No", "No", " ", ""),
        ("No", "No", " additional", "additional"),
        ("No", "Yes", "", "Data Owner approval required"),
        ("No", "Yes", "additional notes", "Data Owner approval required, additional notes"),
        ("Yes", "No", " ", "Supervisor approval required"),
        ("Yes", "Yes", " ", "Supervisor approval required, Data Owner approval required"),
        ("Yes", "Yes", "additional notes", "Supervisor approval required, Data Owner approval required, additional notes"),
    ])
    def test_access_restrictions(self, sup, owner, addl, expected):
        sheet = {
            "B16": MockCell(sup),
            "D16": MockCell(owner),
            "B17": MockCell(addl),
        }
        result = du.access_restrictions("B16", "D16", "B17")(sheet)
        assert_equal(result, expected)

    @parameterized.expand([
        (dt.datetime(1989, 03, 11), "1989-03-11"),
        (dt.date(1989, 03, 11), "1989-03-11"),
        ("1989-03-11", "1989-03-11"),
        ("n/a", ""),
    ])
    def test_date(self, cell_val, expected):
        sheet = {"A1": MockCell(cell_val)}
        result = du.date("A1")(sheet)
        assert_equal(result, expected)

    @parameterized.expand([
        ("Yes", "yes"),
        ("yes", "yes"),
        ("", ""),
        (None, ""),
    ])
    def test_lower(self, cell_val, expected):
        sheet = {"A1": MockCell(cell_val)}
        result = du.lower("A1")(sheet)
        assert_equal(result, expected)

    @parameterized.expand([
        ("", ""),
        ("21", "21"),
        ("2.1", "2.1"),
        ("<1mb", "1"),
        ("foo", ""),
        ("12-13mb", "1213"),
        ("12", "12"),
    ])
    def test_transfer_initial_size(self, cell_val, expected):
        sheet = {"B47": MockCell(cell_val)}
        result = du.transfer_initial_size(sheet)
        assert_equal(result, expected)

    @parameterized.expand([
        ("A39", "foo"),
        (lambda x: x["A39"].value.upper(), "FOO"),
    ])
    def test_get_field(self, cell_or_func, expected):
        fields = {"test": cell_or_func}
        sheet = {"A39": MockCell("foo")}
        result = du.get_field(sheet, "test", fields)
        assert_equal(result, expected)


    @parameterized.expand([
        ("A39", ({"test": "foo"}, [])),
        (lambda ws: v.dig_id_validator(du.strfy(ws["A39"].value)), ({}, ["test: Must be in the format DI#####"])),
    ])
    def test_make_rec_from_sheet(self, cell_or_func, expected):
        fields = {"test": cell_or_func}
        sheet = {"A39": MockCell("foo")}
        result = du.make_rec_from_sheet(sheet, fields)
        assert_equal(result, expected)

