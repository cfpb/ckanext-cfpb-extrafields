import re
import datetime
import json

# Abstracted to simplify unit testing via mock
def Invalid(message):
    try:
        import ckan.plugins.toolkit as tk
        Error = tk.Invalid # pragma: no cover
    except ImportError:
        Error = ValueError # pragma: no cover
    raise Error(message)

def dedupe_unordered(items):
    return list(set(items))

def contains_bad_chars(str):
    ''' contains <>'''
    test = False
    for c in ['>','<']:
        test = test or (c in str)
    return test

def input_value_validator(value):
    # __Other option is the option that triggers a js event for user-specified option creation
    if "__Other" in value :
        Invalid("'Other, please specify' is not a valid option")
    if contains_bad_chars(value):
        Invalid('multi-select fields cannot contain <, > or quote characters')
    # assume that duplicates are mistakes continue quietly
    if not isinstance(value, basestring):
        value = dedupe_unordered(value)
    return value

def pra_control_num_validator(value):
    PRA_CONTROL_NUM_REGEX = re.compile('^\d{4}-\d{4}$')
    if value and not PRA_CONTROL_NUM_REGEX.match(value):
        Invalid("Must be in the format ####-####")
    return value

def dig_id_validator(value):
    DIG_ID_REGEX = re.compile('^DI\d{5}$')
    if value and not DIG_ID_REGEX.match(value):
        Invalid("Must be in the format DI#####")
    return value

def positive_number_validator(value):
    # feels incredibly verbose... requires code review
    if value:
        try:
            if float(value) < 0:
                Invalid("Must be a positive number")
        except ValueError:
            Invalid("Must be a positive number")
    return value

def reasonable_date_validator(value):
    ''' check the year is yyyy-mm-dd and between 1700 and 2300 '''
    if not value:
        return
    parsed_date = to_datetime(value)
    if parsed_date.year < 1700 or parsed_date.year > 2300:
        Invalid("The chosen year is out of range (>1700, <2300).")
    return value

# check multiple fields at once
# http://docs.ckan.org/en/latest/extensions/adding-custom-fields.html#custom-validators
def to_datetime(value):
    if not value:
        return
    try:
        parsed_date = datetime.datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        Invalid("Please ensure date is in yyyy-mm-dd format!")
    return parsed_date

def end_after_start_validator(key, flattened_data, errors, context):
    start_str = flattened_data.get(('content_temporal_range_start',),None)
    end_str = flattened_data.get(('content_temporal_range_end',),None)
    if start_str and end_str:
        if to_datetime(start_str) > to_datetime(end_str):
            Invalid("content start date occurs after end date")
    return

# select multis are contained in unicode strings that look like:
# u'{"blah blah","blah asdf",asdf}' ; u'{asdf,asdf}' ; u'asdf' (see also tests.py)
def clean_select_multi(raw_s):
    ''' parses the results of an html form select-multi '''
    # This solution allows commas, but is unpythonic
    if not raw_s:
        return []
    if not isinstance(raw_s, basestring):
        return raw_s
    s = raw_s.lstrip('{').rstrip('}')
    if s == raw_s:
        return [ s ]
    clean = []
    left = 0
    right = 1
    while right < len(s):
        if s[left]=="\"":
            if right+1<len(s) and s[right]=="\"" and s[right+1]==",":
                # reached the end of the quoted patch; append and skip
                clean.append(s[left+1:right])
                left = right+2
                right = right+3
            else:
                right = right+1
        else:
            if s[right]==",":
                # hit a comma: append and skip the comma
                clean.append(s[left:right])
                left = right+1
                right = right+2
            else:
                right = right+1
    if s[left]=="\"":
        # reached the end with a closing quote (don't save the quotes)
        clean.append(s[left+1:-1])
    else:
        clean.append(s[left:])
    return clean


ROLE_PREFIX = "db_role_level_"
DESC_PREFIX = "db_desc_level_"
def combine_roles(data):
    roles = sorted((key[len(ROLE_PREFIX):], val) for key, val in data.items() if key.startswith(ROLE_PREFIX) and val)
    data["db_roles"] = [[role, data.get(DESC_PREFIX + num, "")] for num, role in roles]

    items_to_delete = [key for key in data.keys() if key.startswith(ROLE_PREFIX) or key.startswith(DESC_PREFIX)]
    for key in items_to_delete:
        del data[key]
    return data
