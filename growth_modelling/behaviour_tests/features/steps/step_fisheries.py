######################################
# Imports
######################################

# External
from behave.runner import Context
from behave import given
from behave import register_type

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

variable_oracle = {
    "total_length" : "stl", "fork_length": "fl", "age": "age"
}

######################################
# Types
######################################

register_type(SnakeCaseString=snake_case_string)
register_type(MaleFemale=parse_male_female)
register_type(CommaList=parse_comma_list)

######################################
# Steps
######################################


@given(
    'our growth curve is a "{growth_curve_longname}" ("{growth_curve:SnakeCaseString}")'
)
def step_impl(context, growth_curve_longname: str, growth_curve: str) -> None:
    context.behaviour.fisheries.growth_curve_longname = growth_curve_longname
    context.behaviour.fisheries.growth_curve = growth_curve
    

@given('our class is "{class_type:SnakeCaseString}"')
def step_impl(context: Context, class_type: str) -> None:
    context.behaviour.fisheries.class_type = class_type


@given('our order is "{order:SnakeCaseString}"')
def step_impl(context: Context, order: str) -> None:
    context.behaviour.fisheries.order = order


@given('our family is "{family:SnakeCaseString}"')
def step_impl(context: Context, family: str) -> None:
    context.behaviour.fisheries.family = family


@given('our species is "{species:SnakeCaseString}"')
def step_impl(context: Context, species: str) -> None:
    context.behaviour.fisheries.species = species


@given('our data source is "{data_source}"')
def step_impl(context: Context, data_source: str) -> None:
    context.behaviour.fisheries.data_source = data_source

@given(u'we define parameter "{parameter:SnakeCaseString}" ("{unit:SnakeCaseString}") as "{description}"')
def step_impl(context: Context, parameter: str, unit: str, description: str) -> None:
    context.behaviour.fisheries.parameters[parameter] = {
        "name": parameter,
        "unit": unit,
        "description": description
    }

@given('we set our random seed to "{random_seed:n}"')
def step_impl(context: Context, random_seed: int):
    context.behaviour.random_seed


@given('our sex is "{sex:MaleFemale}"')
def step_impl(context: Context, sex: str) -> None:
    context.behaviour.fisheries.sex = sex


@given('we have samples taken from "{location_list:CommaList}"')
def step_impl(context: Context, location_list: list[str]) -> None:
    locations = [location_oracle.get(location) for location in location_list]
    context.behaviour.fisheries.locations = locations


@given("recorded location data are unavailable")
def step_impl(context):
    context.behaviour.fisheries.locations = []


@given('we have samples taken between "{lower_date:d}" and "{upper_date:d}"')
def step_impl(context: Context, lower_date: int, upper_date: int) -> None:
    context.behaviour.fisheries.years = [lower_date, upper_date]


@given("recorded year data are unavailable")
def step_impl(context):
    context.behaviour.fisheries.years = []


@given(
    'our response variable is "{response_var:SnakeCaseString}" ("{response_unit:SnakeCaseString}")'
)
def step_impl(context: Context, response_var: str, response_unit: str) -> None:
    response_var = variable_oracle.get(response_var)
    context.behaviour.fisheries.response_var = response_var
    context.behaviour.fisheries.response_unit = response_unit


@given(
    'our explanatory variable is "{explanatory_var:SnakeCaseString}" ("{explanatory_unit:SnakeCaseString}")'
)
def step_impl(context: Context, explanatory_var: str, explanatory_unit: str) -> None:
    explanatory_var = variable_oracle.get(explanatory_var)
    context.behaviour.fisheries.explanatory_var = explanatory_var
    context.behaviour.fisheries.explanatory_unit = explanatory_unit
