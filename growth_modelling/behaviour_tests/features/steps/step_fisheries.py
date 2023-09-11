######################################
# Imports
######################################

from behave import given, when, then, step
from behave import register_type
from parse_type import TypeBuilder

######################################
# Oracles
######################################

location_oracle = {
    "NewSouthWalesA": "nsw1",
    "NewSouthWalesB": "nsw2",
    "QueenslandA": "qld",
    "QueenslandB": "qld2"
}

variable_oracle = {
    "fork_length": "fl",
    "age": "age"
}

######################################
# Types
######################################

def clean_string(text: str) -> str:
    """
    Apply some processing to clean a string.

    Args:
        text (str): 
            The input text.

    Returns:
        str: The cleaned string.
    """
    cleaned_string = (
        text
        .strip()
        .replace(" ", "_")
        .replace(".", "_")
        .lower()
    )
    return cleaned_string
register_type(CleanString=clean_string)

parse_male_female = TypeBuilder.make_enum({"male": "m", "female": "f" })
register_type(MaleFemale = parse_male_female)

def parse_comma_list(text: str) -> list:
    """
    Parse a comma-delimited string into a list.

    Args:
        text (str): 
            The input text.

    Returns:
        list: The parsed list.
    """
    word_list: list[str] = (
        text
        .replace(", and", ",")
        .replace(" ", "")
        .split(",")
    )

    return word_list
register_type(CommaList=parse_comma_list)

######################################
# Steps
######################################

@given('our class is "{class_:CleanString}"')
def step_impl(context, class_: str):
    pass


@given('our order is "{order:CleanString}"')
def step_impl(context, order: str):
    pass


@given('our species is "{species:CleanString}')
def step_impl(context, species: str):
    pass

@given(u'our data source is "{data_source}"')
def step_impl(context, data_source: str):
    pass

@when('our sex is "{sex:MaleFemale}"')
def step_impl(context, sex: str):
    pass

@when('we have samples taken from "{location_list:CommaList}"')
def step_impl(context, location_list: list[str]):
    location_list = [ location_oracle.get(location) for location in location_list ]
    pass

@when('we have samples taken between "{lower_data:d}" and "{upper_date:d}"')
def step_impl(context, lower_data: int, upper_date: int):
    pass

@when('our response variable is "{response_var:CleanString}" ("{response_unit:CleanString}")')
def step_impl(context, response_var: str, response_unit: str):
    response_var = variable_oracle.get(response_var)
    pass

@when('our explanatory variable is "{explanatory_var:CleanString}" ("{explanatory_unit:CleanString}")')
def step_impl(context, explanatory_var: str, explanatory_unit: str):
    explanatory_var = variable_oracle.get(explanatory_var)
    pass