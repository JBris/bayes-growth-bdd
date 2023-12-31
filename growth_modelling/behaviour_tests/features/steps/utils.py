######################################
# Imports
######################################

# External
import arviz as az
from matplotlib import pyplot as plt
import numpy as np
from os.path import join as join_path
import pandas as pd
import pymc as pm
from parse_type import TypeBuilder
from pytensor.tensor import TensorVariable
import xarray as xr

######################################
# Functions
######################################


def get_dir_path(base_dir: str, class_name: str, order: str, species: str) -> str:
    """
    Get the combined directory path.

    Args:
        base_dir (str):
            The base directory.
        class_name (str):
            The taxonomic class.
        order (str):
            The taxonomic order.
        species (str):
             The taxonomic species.

    Returns:
        str: The combined directory path.
    """
    data_dir = join_path(base_dir, class_name, order, species)
    return data_dir


def get_df(
    data_dir: str,
    data_file: str,
    year_interval: list[str],
    sex: str,
    locations: str,
    response_var: str,
    explanatory_var: str,
) -> pd.DataFrame:
    """
    Get the input dataframe.

    Args:
        data_dir (str):
            The input data directory.
        data_file (str):
            The input data file.
        year_interval (list[str]):
            The lower and upper bound for years.
        sex (str):
            The sex of the sample.
        locations (str):
            The locations of the sample.
        response_var (str):
            The model response variable.
        explanatory_var (str):
            The model explanatory variable.

    Returns:
        pd.DataFrame:
            The loaded input dataframe.
    """
    data_file = join_path(data_dir, data_file)
    df = (
        pd.read_csv(data_file)
        .query("sex == @sex")
        .dropna(subset=[response_var, explanatory_var])
    )

    if len(locations) > 0:
        df = df.query("source in @locations")

    if len(year_interval) > 0:
        lower_year, upper_year = year_interval
        df = df.query("year >= @lower_year & year <= @upper_year")

    return df


def fit_model(
    model_type: str,
    model: pm.Model,
    priors: dict,
    x: np.ndarray,
    y: np.ndarray,
    resp: str,
    likelihood: str,
    factors: list[str],
    growth_curve: str = "",
    factor_data: dict[pm.MutableData] = {},
    parameter_factors: dict[list[str]] = {}
) -> None:
    """
    Fit a Bayesian model.

    Args:
        model_type (str):
            The model type.
        model (pm.Model):
            The PyMC model.
        priors (dict):
            The model priors.
        x (np.ndarray):
            The explanatory variable data.
        y (np.ndarray):
            The response variable data.
        resp (str):
            The model response.
        likelihood (str):
            The model likelihood.
        factors (list):
            The list of model factors.
        growth_curve: (str, optional):
            The nonlinear growth curve. Defaults to "".
        factor_data: (dict, optional):
            The factor level data. Defaults to {}.
        parameter_factors (dict[list[str]], optional):
            The map between parameters and factors. Defaults to {}.
    """
    if model_type == "nonlinear":
        fit_nonlinear_model(
            model, priors, x, y, resp, likelihood, factors, 
            growth_curve, factor_data, parameter_factors
        )
    else:
        fit_linear_model(
            model, priors, x, y, resp, likelihood, factors, 
            factor_data, parameter_factors
        )


def vbgm(l_inf: float, k: float, t_0: float, t: np.ndarray) -> np.ndarray:
    """
    Fit a von Bertalanffy growth model.

    Args:
        l_inf (float):
            The asymptotic size.
        k (float):
            The growth coefficient.
        t_0 (float):
            The theoretical age when size is zero.
        t (np.ndarray):
            The age.

    Returns:
        np.ndarray:
            The size at time t.
    """
    L_t = l_inf * (1 - np.exp(-k * (t - t_0)))
    return L_t


def bvbgm(
    l_inf: float, k: float, t_0: float, h: float, t_h: float, t: np.ndarray
) -> np.ndarray:
    """
    Fit a biphasic von Bertalanffy growth model.

    Args:
        l_inf (float):
            The asymptotic size.
        k (float):
            The growth coefficient.
        t_0 (float):
            The theoretical age when size is zero.
        h (float):
            The magnitude of the maximum difference in the size-at-age
            between monophasic and biphasic parameterisations.
        t_h (float):
            The time of the phasic shift.
        t (np.ndarray):
            The age.

    Returns:
        np.ndarray:
            The size at time t.
    """
      
    A_t = 1 - (h / ((t - t_h)** 2 + 1))
    L_t = l_inf * A_t * (1.0 - np.exp(-k * (t - t_0)))
    return L_t


growth_func_map = {"vbgm": vbgm, "bvbgm": bvbgm}


def fit_nonlinear_model(
    model: pm.Model,
    priors: dict,
    x,
    y,
    resp: str,
    likelihood: str,
    factors: list[str],
    growth_curve: str = "",
    factor_data: dict[pm.MutableData] = {},
    parameter_factors: dict[list[str]] = {}
) -> None:
    """
    Fit a nonlinear Bayesian growth model.

    Args:
        model (pm.Model):
            The PyMC model.
        priors (dict):
            The model priors.
        x (np.ndarray):
            The explanatory variable data.
        y (np.ndarray):
            The response variable data.
        resp (str):
            The model response.
        likelihood (str):
            The model likelihood.
        factors (list):
            The list of model factors.
        growth_curve: (str, optional):
            The nonlinear growth curve. Defaults to "".
        factor_data: (dict, optional):
            The factor level data. Defaults to {}.
        parameter_factors (dict[list[str]], optional):
            The map between parameters and factors. Defaults to {}.
    """
    sigma = pm.HalfStudentT("sigma", nu=3, sigma=10)

    growth_func = growth_func_map.get(growth_curve, "vbgm")
    growth_func_kwargs = {"t": x}
    
    for k in priors:
        prior = priors.get(k)

        if "lower" in prior or "upper" in prior:
            growth_func_kwargs[k] = pm.TruncatedNormal(**prior)
        else:
            growth_func_kwargs[k] = pm.Normal(**prior)
        
        factor_levels = parameter_factors.get(k, [])
        for factor in factor_levels:
            alpha_name = f"{k}_{factor}_alpha"
            # Non-centered parameterization for random intercepts.
            mu_a = pm.Normal(f"{alpha_name}_mu", mu=0.0, sigma=prior["sigma"])
            sigma_a = pm.HalfStudentT(f"{alpha_name}_sigma", nu=4, sigma=prior["sigma"])
            z_a = pm.Normal(f"{alpha_name}_z", mu=0, sigma=1, dims=factor)
            alpha = pm.Deterministic(alpha_name, mu_a + z_a * sigma_a, dims=factor)

            indx = factor_data.get(factor)
            growth_func_kwargs[k] += alpha[indx]
        
    if likelihood == "student_t":
        obs = pm.StudentT(
            resp, nu=3, mu=growth_func(**growth_func_kwargs), sigma=sigma, observed=y
        )
    else:
        obs = pm.TruncatedNormal(
            resp, mu=growth_func(**growth_func_kwargs), sigma=sigma, observed=y, lower=0
        )


def fit_linear_model(
    model: pm.Model, priors: dict, x, y, resp: str, likelihood: str, 
    factors: list[str], factor_data: dict[pm.MutableData] = {}, 
    parameter_factors: dict[list[str]] = {}
) -> None:
    """
    Fit a linear Bayesian model.

    Args:
        model (pm.Model):
            The PyMC model.
        priors (dict):
            The model priors.
        x (np.ndarray):
            The explanatory variable data.
        y (np.ndarray):
            The response variable data.
        resp (str):
            The model response.
        likelihood (str):
            The model likelihood.
        factors (list):
            The list of model factors.
        factor_data: (dict, optional):
            The factor level data. Defaults to {}.
        parameter_factors (dict[list[str]], optional):
            The map between parameters and factors. Defaults to {}.
    """
    sigma = pm.HalfStudentT("sigma", nu=3, sigma=10)
    year_indx = factor_data.get("year_indx")
    location_indx = factor_data.get("location_indx")

    intercept_prior = priors.get("intercept")
    slope_prior = priors.get("slope")

    if "lower" in intercept_prior or "upper" in intercept_prior:
        intercept = pm.TruncatedNormal(**intercept_prior)
    else:
        intercept = pm.Normal(**intercept_prior)

    if "lower" in slope_prior or "upper" in slope_prior:
        slope = pm.TruncatedNormal(**slope_prior)
    else:
        slope = pm.Normal(**slope_prior)

    if likelihood == "student_t":
        obs = pm.StudentT(resp, nu=3, mu=intercept + slope * x, sigma=sigma, observed=y)
    else:
        obs = pm.Normal(resp, mu=intercept + slope * x, sigma=sigma, observed=y)


def plot_bayes_model(trace, out_dir: str, hdi_prob: float = 0.95):
    """
    Plot Bayesian modelling results.

    Args:
        trace (Trace):
            The model trace.
        out_dir (str):
            The output directory.
        hdi_prob (float, optional):
            The highest density interval probability. Defaults to 0.95.

    Returns:
        Trace: The model trace.
    """
    textsize = 7
    for plot in ["trace", "rank_vlines", "rank_bars"]:
        az.plot_trace(trace, kind=plot, plot_kwargs={"textsize": textsize})
        outfile = join_path(out_dir, f"{plot}.png")
        plt.tight_layout()
        plt.savefig(outfile)

    def __create_plot(trace, plot_func, plot_name, kwargs):
        plot_func(trace, **kwargs)
        outfile = join_path(out_dir, f"{plot_name}.png")
        plt.tight_layout()
        plt.savefig(outfile)

    kwargs = {
        "figsize": (12, 12),
        "scatter_kwargs": dict(alpha=0.01),
        "marginals": True,
        "textsize": textsize,
    }
    __create_plot(trace, az.plot_pair, "marginals", kwargs)

    kwargs = {"figsize": (12, 12), "textsize": textsize}
    __create_plot(trace, az.plot_violin, "violin", kwargs)

    kwargs = {"figsize": (12, 12), "textsize": 5}
    __create_plot(trace, az.plot_posterior, "posterior", kwargs)

    outfile = join_path(out_dir, "summary.csv")
    az.summary(trace, hdi_prob=hdi_prob).to_csv(outfile)

    pm.sample_posterior_predictive(trace, extend_inferencedata=True, progressbar=False)

    kwargs = {"figsize": (12, 12), "textsize": textsize}
    __create_plot(trace, az.plot_ppc, "ppc", kwargs)

    return trace


def get_mu_pp(
    trace, model_type: str, x: np.ndarray, priors: dict, growth_curve: str = ""
) -> xr.DataArray:
    """
    Get the mean posterior predictions.

    Args:
        trace (Trace):
            The model trace.
        model_type (str):
            The model type.
        x (np.ndarray):
            The explanatory variable values.
        priors (dict):
            The model priors.
        growth_curve: (str):
            The nonlinear growth curve.

    Returns:
        xr.DataArray: The mean posterior predictions.
    """
    post = trace.posterior

    if model_type == "nonlinear":
        kwargs = {"t": xr.DataArray(x, dims=["obs_id"])}
        for k in priors:
            kwargs[k] = post[k]

        growth_func = growth_func_map.get(growth_curve, "vbgm")
        mu_pp = growth_func(**kwargs)
    else:
        mu_pp = post["intercept"] + post["slope"] * xr.DataArray(x, dims=["obs_id"])

    return mu_pp


def plot_preds(
    mu_pp,
    out_dir: str,
    observed_data,
    posterior_predictive,
    x: np.ndarray,
    response_var: str,
    explanatory_var: str,
    hdi_prob: float = 0.95,
) -> str:
    """
    Plot predicted values over the observations.

    Args:
        mu_pp (DataArray):
            The mean posterior predictions.
        out_dir (str):
            The output directory.
        observed_data (DataArray):
            The observed data.
        posterior_predictive (DataArray):
            The posterior predictions.
        x (np.ndarray):
            The explanatory variable values.
        response_var (str):
            The response variable.
        explanatory_var (str):
            The explanatory variable
        hdi_prob (float, optional):
            The highest density interval probability. Defaults to 0.95.

    Returns:
        str: The output file.
    """
    _, ax = plt.subplots()

    ax.plot(
        x,
        mu_pp.mean(("chain", "draw")),
        label=f"Mean {response_var}",
        color="C1",
        alpha=0.6,
    )
    ax.scatter(x, observed_data)
    az.plot_hdi(x, posterior_predictive, hdi_prob=hdi_prob)

    ax.set_xlabel(explanatory_var)
    ax.set_ylabel(response_var)
    plt.tight_layout()
    outfile = join_path(out_dir, f"{response_var}_{explanatory_var}.png")
    plt.savefig(outfile)
    return outfile


def get_trace_dict_key(
    class_type: str,
    order: str,
    species: str,
    sex: str,
    model_type: str,
    growth_curve: str,
) -> str:
    """
    Get the dictionary key for the Bayesian model trace.

    Args:
        class_type (str):
            The taxonomic class.
        order (str):
            The taxonomic order.
        species (str):
            The taxonomic species.
        sex (str):
            The sex of the animal.
        model_type (str):
            The type of model being fitted.
        growth_curve (str):
            The type of growth curve being fitted.

    Returns:
        str:
            The dictionary key
    """
    trace_key = "_".join(
        [class_type, order, species, sex, model_type, growth_curve]
    )
    return trace_key


def snake_case_string(text: str) -> str:
    """
    Apply some processing to convert a string to snakecase.

    Args:
        text (str):
            The input text.

    Returns:
        str: The snakecase string.
    """
    snake_string = (
        text.strip().replace(" ", "_").replace(".", "_").replace("-", "_").lower()
    )
    return snake_string


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
        text.replace(", and", ",").replace(" and ", ",").replace(" ", "").split(",")
    )

    return word_list


######################################
# Types
######################################

parse_comparison = TypeBuilder.make_enum(
    {"greater than": ">", "less than": "<", "equal to": "=="}
)
parse_enabled_disabled = TypeBuilder.make_enum({"enabled": True, "disabled": False})
parse_male_female = TypeBuilder.make_enum({"male": "m", "female": "f"})
