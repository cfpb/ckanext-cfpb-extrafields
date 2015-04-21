import re

# Abstracted to simplify unit testing via mock
def Invalid(message):
    import ckan.plugins.toolkit as tk
    raise tk.Invalid(message)

def dedupe_unordered(items):
    return list(set(items))
def contains_bad_chars(str):
    ''' contains \"{},'''
    test = False
    for c in ['\"','{','}',',']:
        test = test or (c in str)
    return test
def input_value_validator(value):
    if "__Other" in value :
        Invalid("'Other, please specify' is not a valid option")
#    if contains_bad_chars(value):
#        Invalid('multi-select fields cannot contain commas, {}, or double-quotes')
    # assume that duplicates are mistakes continue quietly
    if not isinstance(value, basestring):
        value = dedupe_unordered(value)
    return value

# check multiple fields at once
# http://docs.ckan.org/en/latest/extensions/adding-custom-fields.html#custom-validators
def check_all(key, flattened_data, errors, context):
    return

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
    ''' check the year is between 1700 and 2300 '''
# TODO: this doesn't work as expected. Feels like a CKAN bug with custom resource fields.
#     if value:
#         date = int(value.replace('-',''))
#         if date < 1700*10000 or date > 2300*10000:
#             print 'this does not work!'+str(date)+value
#             Invalid("The chosen year is out of range.")
#         return value
#     else: 
#         return value
    return value

