#!/usr/bin/python

######################################
# Imports
######################################

# External
import hydra
from omegaconf import DictConfig
from os.path import join as join_path
import pandas as pd
from pathlib import Path

######################################
# Main
######################################


def write_species_csv(
    species_code: str,
    index_df: pd.DataFrame,
    data_dir: str,
    cols: str,
    outfile: str,
    lowercase_list=[],
    drop_na=False,
) -> None:
    """
    Creates a species dataframe and writes it to a CSV file.

    Args:
        species_code (str):
            The shark species code.
        index_df (pd.DataFrame):
            The index dataframe containing metadata.
        data_dir (str):
            The data directory.
        cols (str):
            The dataframe column list.
        outfile (str):
            The output file name.
        lowercase_list (list, optional):
            Columns to convert all values to lowercase.
        drop_na (bool, optional):
            Drop missing values
    """
    species_df = index_df.query("species_code == @species_code")
    extract_val = lambda key: species_df[key].values.item()

    species = extract_val("species")
    class_ = extract_val("class")
    order = extract_val("order")

    # Make dirs
    out_dir = join_path(data_dir, class_, order, species)
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Load data
    dataset_file = extract_val("dataset")
    data_path = join_path(data_dir, dataset_file)
    species_code = species_code.upper()
    data_df = pd.read_csv(data_path).query("Species == @species_code")

    # Preprocess
    data_df["age"] = data_df["AgeAgree"]
    data_df.columns = data_df.columns.str.lower()
    data_df = data_df[cols]
    if drop_na:
        data_df = data_df.dropna(axis=0)
    for lower_col in lowercase_list:
        data_df[lower_col] = data_df[lower_col].astype("str").str.lower()

    # Write data
    outfile = join_path(out_dir, outfile)
    data_df.to_csv(outfile, index=False)

    source = extract_val("source")
    outfile = join_path(out_dir, "README.md")
    with open(outfile, "w+") as f:
        f.writelines(source)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(config: DictConfig) -> None:
    """
    The main entry point for the preprocess pipeline.

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

    preprocess_config = config["preprocess"]
    COLS = preprocess_config["cols"]
    DROP_NA = preprocess_config["drop_na"]
    LOWERCASE = preprocess_config["lowercase"]

    # Load data
    index_file = join_path(DATA_DIR, INDEX)
    index_df = pd.read_csv(index_file)

    for species_code in SPECIES_LIST:
        write_species_csv(
            species_code, index_df, DATA_DIR, COLS, OUTFILE, LOWERCASE, DROP_NA
        )


if __name__ == "__main__":
    main()
