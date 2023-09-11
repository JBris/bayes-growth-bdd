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
import xarray as xr

######################################
# Oracles
######################################

likelihood_oracle = {
    "gaussian": pm.Normal
}

######################################
# Functions
######################################

def get_dir_path(base_dir: str, class_: str, order: str, species: str) -> str:
    """
    Get the combined directory path.

    Args:
        base_dir (str): 
            The base directory.
        class_ (str): 
            The taxonomic class.
        order (str): 
            The taxonomic order.
        species (str):
             The taxonomic species.

    Returns:
        str: The combined directory path.
    """
    data_dir = join_path(base_dir, class_, order, species) 
    return data_dir


def get_df(
        data_dir: str, data_file: str, year_interval: list[str], sex: str, locations: str,
        response_var: str, explanatory_var: str
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
    lower_year, upper_year = year_interval

    df = (
        pd.read_csv(data_file)
        .query("sex == @sex")
        .query("source in @locations")
        .query("year >= @lower_year & year <= @upper_year")
        .dropna(subset = [response_var, explanatory_var])
    )

    return df

def fit_model(
    model_type: str, model: pm.Model, priors: dict, x: np.ndarray, y: np.ndarray, 
    resp: str, likelihood: str
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
    """
    fit_linear_model(model, priors, x, y, resp, likelihood)

def fit_linear_model(model: pm.Model, priors: dict, x, y, resp: str, likelihood: str) -> None:
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
    """
    sigma = pm.HalfStudentT("sigma", nu = 3, sigma = 10)
    intercept = pm.Normal(**priors.get("intercept"))
    slope = pm.Normal(**priors.get("slope"))

    model_likelihood = likelihood_oracle.get(likelihood)
    obs = model_likelihood(resp, mu=intercept + slope * x, sigma=sigma, observed=y)

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
        az.plot_trace(trace, kind = plot, plot_kwargs = {"textsize": textsize})
        outfile = join_path(out_dir, f"{plot}.png")
        plt.tight_layout()
        plt.savefig(outfile)

    def __create_plot(trace, plot_func, plot_name, kwargs):
        plot_func(trace, **kwargs)
        outfile = join_path(out_dir, f"{plot_name}.png")
        plt.tight_layout()
        plt.savefig(outfile)
    
    kwargs = {"figsize": (12, 12), "scatter_kwargs": dict(alpha = 0.01), "marginals": True, "textsize": textsize}
    __create_plot(trace, az.plot_pair, "marginals", kwargs)

    kwargs = {"figsize": (12, 12), "textsize": textsize}
    __create_plot(trace, az.plot_violin, "violin", kwargs)

    kwargs = {"figsize": (12, 12), "textsize": 5}
    __create_plot(trace, az.plot_posterior, "posterior", kwargs)

    outfile = join_path(out_dir, "summary.csv")
    az.summary(trace, hdi_prob = hdi_prob).to_csv(outfile)

    pm.sample_posterior_predictive(trace, extend_inferencedata=True)

    kwargs = {"figsize": (12, 12), "textsize": textsize}
    __create_plot(trace, az.plot_ppc, "ppc", kwargs)

    return trace

def get_mu_pp(trace, model_type: str, x: np.ndarray) -> xr.DataArray:
    """
    Get the mean posterior predictions.

    Args:
        trace (Trace): 
            The model trace.
        model_type (str): 
            The model type.
        x (np.ndarray): 
            The explanatory variable values.

    Returns:
        xr.DataArray: The mean posterior predictions.
    """
    post = trace.posterior
    mu_pp = post["intercept"] + post["slope"] * xr.DataArray(x, dims=["obs_id"])

    return mu_pp

def plot_preds(
    mu_pp, out_dir: str, observed_data, posterior_predictive, x: np.ndarray, 
    response_var: str, explanatory_var: str, hdi_prob: float = 0.95
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
        x, mu_pp.mean(("chain", "draw")), label=f"Mean {response_var}", color="C1", alpha=0.6
    )
    ax.scatter(x, observed_data)
    az.plot_hdi(x, posterior_predictive, hdi_prob = hdi_prob)

    ax.set_xlabel(explanatory_var)
    ax.set_ylabel(response_var)
    plt.tight_layout()
    outfile = join_path(out_dir, f"{response_var}_{explanatory_var}.png")
    plt.savefig(outfile)
    return outfile

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
        text
        .strip()
        .replace(" ", "_")
        .replace(".", "_")
        .replace("-", "_")
        .lower()
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
        text
        .replace(", and", ",")
        .replace(" ", "")
        .split(",")
    )

    return word_list

######################################
# Types
######################################

parse_comparison = TypeBuilder.make_enum({"greater than": ">", "less than": "<", "equal": "=="})
parse_enabled_disabled = TypeBuilder.make_enum({"enabled": True, "disabled": False})
parse_male_female = TypeBuilder.make_enum({"male": "m", "female": "f"})
