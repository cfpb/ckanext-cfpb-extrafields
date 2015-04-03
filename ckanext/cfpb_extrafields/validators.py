import re

PRA_CONTROL_NUM_REGEX = re.compile('^\d{4}-\d{4}$')

# Abstracted to simplify unit testing via mock
def Invalid(message):
    import ckan.plugins.toolkit as tk
    raise tk.Invalid(message)

def dedupe_unordered(items):
    return list(set(items))

def is_alphanumeric_plus(str):
    '''Check that characters are alphanumeric or [space,_,-].'''
    return re.match('^[-\w ]+$', str) is not None

def input_value_validator(value):
    if "__Other" in value :
        Invalid("Please unselect all 'Other' fields")
    if not is_alphanumeric(value):
        Invalid('Specified "Other" field cannot include special characters')
    # assume that duplicates are mistakes continue quietly
    value = dedupe_unordered(value)
    return value

# check multiple fields at once
# http://docs.ckan.org/en/latest/extensions/adding-custom-fields.html#custom-validators
def check_all(key, flattened_data, errors, context):
    return

def pra_control_num_validator(value):
    if value and not PRA_CONTROL_NUM_REGEX.match(value):
        Invalid("Must be in the format XXXX-XXXX")
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



