######################################
# Imports
######################################

# External
from behave.runner import Context
from behave import given, when
from behave import register_type
from parse_type import TypeBuilder

# Internal
from utils import parse_comma_list, parse_male_female, snake_case_string

######################################
# Oracles
######################################

location_oracle = {
    "NewSouthWalesA": "nsw1",
    "NewSouthWalesB": "nsw2",
    "QueenslandA": "qld",
    "QueenslandB": "qld2",
}

variable_oracle = {"fork_length": "fl", "age": "age"}

######################################
# Types
######################################

register_type(SnakeCaseString=snake_case_string)
register_type(MaleFemale=parse_male_female)
register_type(CommaList=parse_comma_list)

######################################
# Steps
######################################


@given('our class is "{class_:SnakeCaseString}"')
def step_impl(context: Context, class_: str) -> None:
    context.behaviour.fisheries.class_ = class_


@given('our order is "{order:SnakeCaseString}"')
def step_impl(context: Context, order: str) -> None:
    context.behaviour.fisheries.order = order


@given('our species is "{species:SnakeCaseString}"')
def step_impl(context: Context, species: str) -> None:
    context.behaviour.fisheries.species = species


@given('our data source is "{data_source}"')
def step_impl(context: Context, data_source: str) -> None:
    context.behaviour.fisheries.data_source = data_source


@when('our sex is "{sex:MaleFemale}"')
def step_impl(context: Context, sex: str) -> None:
    context.behaviour.fisheries.sex = sex

@when('we have samples taken from "{location_list:CommaList}"')
def step_impl(context: Context, location_list: list[str]) -> None:
    locations = [location_oracle.get(location) for location in location_list]
    context.behaviour.fisheries.locations = locations

@when('we have samples taken between "{lower_data:d}" and "{upper_date:d}"')
def step_impl(context: Context, lower_data: int, upper_date: int) -> None:
    context.behaviour.fisheries.years = (lower_data, upper_date)


@when(
    'our response variable is "{response_var:SnakeCaseString}" ("{response_unit:SnakeCaseString}")'
)
def step_impl(context: Context, response_var: str, response_unit: str) -> None:
    response_var = variable_oracle.get(response_var)
    context.behaviour.fisheries.response_var = response_var
    context.behaviour.fisheries.response_unit = response_unit

@when(
    'our explanatory variable is "{explanatory_var:SnakeCaseString}" ("{explanatory_unit:SnakeCaseString}")'
)
def step_impl(context: Context, explanatory_var: str, explanatory_unit: str) -> None:
    explanatory_var = variable_oracle.get(explanatory_var)
    context.behaviour.fisheries.explanatory_var = explanatory_var
    context.behaviour.fisheries.explanatory_unit = explanatory_unit
