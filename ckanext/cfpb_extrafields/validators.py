import re

PRA_CONTROL_NUM_REGEX = re.compile('^\d{4}-\d{4}$')

# Abstracted to simplify unit testing via mock
def Invalid(message):
    import ckan.plugins.toolkit as tk
    raise tk.Invalid(message)


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



