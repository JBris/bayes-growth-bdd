######################################
# Imports
######################################

# External
import arviz as az
from behave.runner import Context
from behave import given, when, then
from behave import register_type
from matplotlib import pyplot as plt
from os.path import join as join_path
import pymc as pm

# Internal
from utils import (
    fit_model,
    get_dir_path,
    get_df,
    get_mu_pp,
    get_trace_dict_key,
    parse_comparison,
    parse_enabled_disabled,
    plot_bayes_model,
    plot_preds,
    snake_case_string,
    parse_comma_list,
)

######################################
# Oracles
######################################

factor_oracle = {"year": "year", "location": "source"}

######################################
# Types
######################################

register_type(QueryComparison=parse_comparison)
register_type(EnabledDisabled=parse_enabled_disabled)
register_type(SnakeCaseString=snake_case_string)
register_type(CommaList=parse_comma_list)

######################################
# Functions
######################################

def get_trace_key(context: Context, growth_curve: str = "") -> str:
    """
    Get the dictionary key for the trace object from the test context.

    Args:
        context (Context): 
            The test context.
        growth_curve (str, optional): 
            The growth curve dictionary key. Defaults to "".

    Returns:
        str: 
            The dictionary key for the trace object.
    """
    bayesian_def = context.behaviour.bayesian
    fisheries_def = context.behaviour.fisheries

    if growth_curve == "":
        growth_curve = fisheries_def.growth_curve

    trace_key = get_trace_dict_key(
        fisheries_def.class_type,
        fisheries_def.order,
        fisheries_def.species,
        fisheries_def.sex,
        bayesian_def.model_type,
        growth_curve,
    )

    return trace_key

######################################
# Steps
######################################

@given(
    'we are fitting a "{model_type}" Bayesian multilevel growth model using "{sampler_longname}" ("{sampler: SnakeCaseString}")'
)
def step_impl(
    context: Context, model_type: str, sampler_longname: str, sampler: str
) -> None:
    context.behaviour.bayesian.model_type = model_type
    context.behaviour.bayesian.sampler_longname = sampler_longname
    context.behaviour.bayesian.sampler = sampler


@given(
    'we are fitting a growth model with a "{likelihood: SnakeCaseString}" likelihood'
)
def step_impl(context: Context, likelihood: str) -> None:
    context.behaviour.bayesian.likelihood = likelihood


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


@given('we retrieve our data from the "{data_file}" file')
def step_impl(context: Context, data_file: str) -> None:
    context.behaviour.data_file = data_file


@given(
    'we believe that the "{parameter:SnakeCaseString}" parameter could plausibly be "{mu:f}" with a standard deviation of "{sigma:f}"'
)
def step_impl(context: Context, parameter: str, mu: float, sigma: float) -> None:
    context.behaviour.bayesian.priors[parameter] = {
        "name": parameter,
        "mu": mu,
        "sigma": sigma,
    }


@given(
    'we believe that the "{parameter:SnakeCaseString}" parameter could plausibly be "{mu:f}" with a standard deviation of "{sigma:f}" and a "{bound_key:SnakeCaseString}" bound of "{bound}"'
)
def step_impl(
    context: Context,
    parameter: str,
    mu: float,
    sigma: float,
    bound_key: str,
    bound: float,
):
    prior = {"name": parameter, "mu": mu, "sigma": sigma}
    prior[bound_key] = bound
    context.behaviour.bayesian.priors[parameter] = prior


@given('we fit random intercepts to "{factor_list:CommaList}"')
def step_impl(context, factor_list: list[str]) -> None:
    factors = [factor_oracle.get(factor) for factor in factor_list]
    context.behaviour.bayesian.factors = factors


@given(
    'we aim to evaluate the "{hdi_prob:f}" highest posterior density intervals (HDIs) of our parameter estimates'
)
def step_impl(context: Context, hdi_prob: float) -> None:
    context.behaviour.bayesian.hdi_prob = hdi_prob


@given('our assessment metric is "{metric_longname}" ("{metric:SnakeCaseString}")')
def step_impl(context: Context, metric_longname: str, metric: str) -> None:
    context.behaviour.bayesian.metric_longname = metric_longname
    context.behaviour.bayesian.metric = metric


@given('our assessment method is "{method_longname}" ("{method:SnakeCaseString}")')
def step_impl(context: Context, method_longname: str, method: str) -> None:
    context.behaviour.bayesian.method_longname = method_longname
    context.behaviour.bayesian.method = method


@given('our method to estimate the model weights is "{model_weights}"')
def step_impl(context: Context, model_weights: str) -> None:
    context.behaviour.bayesian.model_weights = model_weights


@when("we fit our Bayesian model")
def step_impl(context: Context) -> None:
    behaviour = context.behaviour
    bayesian_def = behaviour.bayesian
    fisheries_def = behaviour.fisheries

    data_dir = get_dir_path(
        behaviour.data_dir,
        fisheries_def.class_type,
        fisheries_def.order,
        fisheries_def.species,
    )

    df = get_df(
        data_dir,
        behaviour.data_file,
        fisheries_def.years,
        fisheries_def.sex,
        fisheries_def.locations,
        fisheries_def.response_var,
        fisheries_def.explanatory_var,
    )

    out_dir = join_path(
        "out",
        fisheries_def.class_type,
        fisheries_def.order,
        fisheries_def.species,
        fisheries_def.sex,
        bayesian_def.model_type,
        fisheries_def.growth_curve,
    )

    x = df[fisheries_def.explanatory_var].values
    y = df[fisheries_def.response_var].values
    resp = "y"
    with pm.Model() as model:
        fit_model(
            bayesian_def.model_type,
            model,
            bayesian_def.priors,
            x,
            y,
            resp,
            bayesian_def.likelihood,
            bayesian_def.factors,
            fisheries_def.growth_curve,
        )

        if bayesian_def.parallelisation:
            cores = bayesian_def.n_chains
        else:
            cores = 1

        trace = pm.sample(
            draws=bayesian_def.n_draws,
            tune=bayesian_def.n_burn,
            chains=bayesian_def.n_chains,
            cores=cores,
            target_accept=bayesian_def.acceptance_prob,
            model=model,
            random_seed=behaviour.random_seed,
            progressbar=False,
        )
        pm.compute_log_likelihood(trace)
        trace = plot_bayes_model(trace, out_dir, bayesian_def.hdi_prob)

        mu_pp = get_mu_pp(
            trace,
            bayesian_def.model_type,
            x,
            bayesian_def.priors,
            fisheries_def.growth_curve,
        )
        plot_preds(
            mu_pp,
            out_dir,
            trace.observed_data[resp],
            trace.posterior_predictive[resp],
            x,
            fisheries_def.response_var,
            fisheries_def.explanatory_var,
            bayesian_def.hdi_prob,
        )

        trace_key = get_trace_key(context)
        context.traces[trace_key] = trace

        behaviour.to_yaml(out_dir)

@when('we compare the following candidate models "{growth_curve_list:CommaList}"')
def step_impl(context: Context, growth_curve_list: list[str]) -> None:
    behaviour = context.behaviour
    bayesian_def = behaviour.bayesian
    fisheries_def = behaviour.fisheries
    candidate_models = {}

    for k in growth_curve_list:
        trace_key = get_trace_key(context, k.lower())
        candidate_models[k] = context.traces[trace_key]

    model_scores_df = az.compare(
        candidate_models, ic = bayesian_def.method, method = bayesian_def.model_weights
    )
    model_scores_df["model"] = model_scores_df.index

    out_dir = join_path(
        "out",
        fisheries_def.class_type,
        fisheries_def.order,
        fisheries_def.species,
        fisheries_def.sex,
        bayesian_def.model_type,
    )

    outfile = join_path(out_dir, "model_scores.csv")
    model_scores_df.to_csv(outfile, index=False)

    outfile = join_path(out_dir, "model_scores.png")
    az.plot_compare(
        model_scores_df, plot_standard_error=True, plot_ic_diff=True, order_by_rank=True, legend=True, title=True
    )
    plt.savefig(outfile)

    context.model_scores = model_scores_df

@then(
    'we expect our "{diag_longname}" ("{diagnostic:SnakeCaseString}") diagnostics to all be "{comparison:QueryComparison}" "{diag_baseline:f}"'
)
def step_impl(
    context: Context,
    diag_longname: str,
    diagnostic: str,
    comparison: str,
    diag_baseline: float,
) -> None:
    trace_key = get_trace_key(context)
    trace = context.traces[trace_key]

    hdi_prob = context.behaviour.bayesian.hdi_prob
    trace_df = az.summary(trace, hdi_prob=hdi_prob)
    n_rows = trace_df.shape[0]

    filtered_df = trace_df.query(f"{diagnostic} {comparison} @diag_baseline")
    filtered_n_rows = filtered_df.shape[0]

    assert n_rows == filtered_n_rows


@then(
    'we expect the posterior mean of the "{parameter}" parameter estimate to be "{estimate:f}" with "{error_prop:f}" error'
)
def step_impl(
    context: Context, parameter: str, estimate: float, error_prop: float
) -> None:
    trace_key = get_trace_key(context)
    trace = context.traces[trace_key]

    hdi_prob = context.behaviour.bayesian.hdi_prob
    trace_df = az.summary(trace, hdi_prob=hdi_prob)
    trace_df["parameter"] = trace_df.index

    error = estimate * error_prop
    posterior_mean = trace_df.query("parameter == @parameter")["mean"].values.item()

    assert posterior_mean < (estimate + error) and posterior_mean > (estimate - error)
