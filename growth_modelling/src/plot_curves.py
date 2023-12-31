#!/usr/bin/python

######################################
# Imports
######################################

# External
import hydra
from matplotlib import pyplot as plt
from omegaconf import DictConfig
from os.path import join as join_path
import pandas as pd
import seaborn as sns

######################################
# Main
######################################


def plot_curves(
    species_code: str,
    index_df: pd.DataFrame,
    data_dir: str,
    infile: str,
    x: str,
    y: str,
    hue: str,
    col: str,
    as_cat: list[str] = [],
    tracking_uri: str = None,
    enable_experiment_tracking: bool = False
) -> None:
    """
    Plot the growth curves.

    Args:
        species_code (str):
            The shark species code.
        index_df (pd.DataFrame):
            The index dataframe containing metadata.
        data_dir (str):
            The data directory.
        infile (str):
            The input datafile.
        x (str):
            The x column.
        y (str):
            The y column.
        hue (str):
            The grouping column.
        col (str):
            The categorical column.
        as_cat (list[str], optional):
            Cast the column as a category. Defaults to [].
        tracking_uri (str, optional):
            The experiment tracking URI. Defaults to None.
        enable_experiment_tracking (bool, optional):
            Enable experiment tracking. Defaults to False.
    """
    species_df = index_df.query("species_code == @species_code")
    extract_val = lambda key: species_df[key].values.item()

    species = extract_val("species")
    class_type = extract_val("class")
    order = extract_val("order")

    in_dir = join_path(data_dir, class_type, order, species)
    datafile = join_path(in_dir, infile)
    data_df = pd.read_csv(datafile)

    for cat_col in as_cat:
        data_df[cat_col] = data_df[cat_col].astype("category")

    sns.catplot(
        x=x,
        y=y,
        hue=hue,
        col=col,
        col_wrap=3,
        data=data_df,
        kind="point",
        height=4,
        aspect=0.8,
    )
    outfile = join_path(in_dir, f"{y}_{x}.png")
    plt.savefig(outfile)

    if enable_experiment_tracking is False or tracking_uri is None:
        return

    import mlflow

    mlflow.set_tracking_uri(tracking_uri)
    experiment_name = "plot_growth_curves"
    existing_exp = mlflow.get_experiment_by_name(experiment_name)
    if not existing_exp:
        mlflow.create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)
    mlflow.set_tag("species", species)

    mlflow.log_param("species", species)
    mlflow.log_param("class", class_type)
    mlflow.log_param("order", order)

    def log_series(df, interval=0.01):
        series = df[y].dropna().sort_values().values
        series_interval = int(len(series) * interval)
        for i, value in enumerate(series):
            if i % series_interval != 0:
                continue
            mlflow.log_metric(y, value, step=i)

    data_df.groupby(hue).apply(log_series)

    mlflow.log_artifact(outfile)
    mlflow.end_run()


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(config: DictConfig) -> None:
    """
    The main entry point for the plotting pipeline.

    Args:
        config (DictConfig):
            The pipeline configuration.
    """
    # Constants
    SPECIES_LIST = config["common"]["species"]
    TRACKING_URI = config["experiment_tracking"]["tracking_uri"]
    ENABLE_EXPERIMENT_TRACKING = config["experiment_tracking"]["enabled"]

    data_config = config["data"]
    DATA_DIR = data_config["dir"]
    INDEX = data_config["index"]
    OUTFILE = data_config["out"]

    plot_config = config["plot"]
    X = plot_config["x"]
    Y = plot_config["y"]
    HUE = plot_config["hue"]
    COL = plot_config["col"]
    AS_CAT = plot_config["as_cat"]

    # Load data
    index_file = join_path(DATA_DIR, INDEX)
    index_df = pd.read_csv(index_file)

    for species_code in SPECIES_LIST:
        plot_curves(
            species_code,
            index_df,
            DATA_DIR,
            OUTFILE,
            X,
            Y,
            HUE,
            COL,
            AS_CAT,
            TRACKING_URI,
            ENABLE_EXPERIMENT_TRACKING
        )


if __name__ == "__main__":
    main()
