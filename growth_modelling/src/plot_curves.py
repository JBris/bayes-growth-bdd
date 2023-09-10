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
    species_code: str, index_df: pd.DataFrame, data_dir: str, infile: str, x: str, 
    y: str, hue: str, col: str, as_cat: list[str] = []
) -> None:
    species_df = index_df.query("species_code == @species_code")
    extract_val = lambda key: species_df[key].values.item()

    species = extract_val("species")
    class_ = extract_val("class")
    order = extract_val("order")

    in_dir = join_path(data_dir, class_, order, species)
    datafile = join_path(in_dir, infile)
    data_df = pd.read_csv(datafile)

    for cat_col in as_cat:
        data_df[cat_col] = data_df[cat_col].astype("category")
    
    g = sns.catplot(
        x=x,
        y=y,
        hue=hue,
        col=col,
        col_wrap=3, 
        data=data_df,
        kind='point',
        height=4,
        aspect=.8
    )
    outfile = join_path(in_dir, f"{y}_{x}.png")
    plt.savefig(outfile)

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
        plot_curves(species_code, index_df, DATA_DIR, OUTFILE, X, Y, HUE, COL, AS_CAT)

if __name__ == "__main__":
    main()
