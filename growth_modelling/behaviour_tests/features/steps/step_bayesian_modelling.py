######################################
# Imports
######################################

from behave import given, when, then, step
from behave import register_type
from parse_type import TypeBuilder

######################################
# Types
######################################

parse_enabled_disabled = TypeBuilder.make_enum({"enabled": True, "disabled": False })
register_type(EnabledDisabled = parse_enabled_disabled)

######################################
# Steps
######################################

@given('we are fitting a "{model_type}" Bayesian multilevel model using "{sampler}"')
def step_impl(context, model_type, sampler):
    print(model_type)
    pass

@given('we are running "{n_chains:d}" Markov chain Monte Carlo (MCMC) chains with parallelisation "{enabled:EnabledDisabled}"')
def step_impl(context, n_chains: int, enabled: bool):
    pass

@given('we are taking "{n_draws:d}" draws per MCMC chain')
def step_impl(context, n_draws: int):
    pass

@given('we specify "{n_burn:d}" samples for our burn-in period')
def step_impl(context, n_burn: int):
    pass


@given('our MCMC samples have an acceptance probability of "{tree_accept:f}"')
def step_impl(context, tree_accept: float):
    pass


