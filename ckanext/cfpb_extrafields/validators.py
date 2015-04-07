import re

# Abstracted to simplify unit testing via mock
def Invalid(message):
    import ckan.plugins.toolkit as tk
    raise tk.Invalid(message)

def dedupe_unordered(items):
    return list(set(items))

def is_alphanumeric_plus(str):
    '''Check that all characters are are alphanumeric or [space,_,-].'''
    # make sure input is a string before matching
    return re.match('^[-\w ]+$', ''.join(str)) is not None

def input_value_validator(value):
    if "__Other" in value :
        Invalid("Please unselect 'Other' from drop down menus")
    if not is_alphanumeric_plus(value):
        Invalid('Specified "Other" field cannot include most special characters')
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



