######################################
# Imports
######################################

# External
from behave.runner import Context
from behave import given, when
from behave import register_type

# Internal
from utils import parse_enabled_disabled, snake_case_string

######################################
# Oracles
######################################

######################################
# Types
######################################

register_type(EnabledDisabled=parse_enabled_disabled)
register_type(SnakeCaseString=snake_case_string)

######################################
# Steps
######################################


@given('we are fitting a "{model_type}" Bayesian multilevel model using "{sampler_longname}" ("{sampler: SnakeCaseString}")')
def step_impl(context: Context, model_type: str, sampler_longname: str, sampler: str) -> None:
    context.behaviour.bayesian.model_type = model_type
    context.behaviour.bayesian.sampler_longname = sampler_longname
    context.behaviour.bayesian.sampler = sampler

@given(
    'we are running "{n_chains:d}" Markov chain Monte Carlo (MCMC) chains with parallelisation "{parallelisation:EnabledDisabled}"'
)
def step_impl(context: Context, n_chains: int, parallelisation: bool) -> None:
    context.behaviour.bayesian.n_chains = n_chains
    context.behaviour.bayesian.parallelisation = parallelisation

@given('we are taking "{n_draws:d}" draws per MCMC chain')
def step_impl(context: Context, n_draws: int) -> None:
    context.behaviour.bayesian.n_draws = n_draws

@given('we specify "{n_burn:d}" samples for our burn-in period')
def step_impl(context: Context, n_burn: int) -> None:
    context.behaviour.bayesian.n_burn = n_burn

@given('our MCMC samples have an acceptance probability of "{acceptance_prob:f}"')
def step_impl(context: Context, acceptance_prob: float) -> None:
    context.behaviour.bayesian.acceptance_prob = acceptance_prob

@when(u'we retrieve our data from "{data_file}"')
def step_impl(context: Context, data_file: str) -> None:
    context.behaviour.data_file = data_file

@when("we fit our Bayesian multilevel model")
def step_impl(context: Context) -> None:
    from os.path import join as join_path
    import pandas as pd

    behaviour = context.behaviour
    bayesian_def = behaviour.bayesian
    fisheries_def = behaviour.fisheries 

    data_dir = join_path(behaviour.data_dir, fisheries_def.class_, fisheries_def.order, fisheries_def.species) 
    data_file = join_path(data_dir, behaviour.data_file)

    df = pd.read_csv(data_file)
    raise NotImplementedError(df)
