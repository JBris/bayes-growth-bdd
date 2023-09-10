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
    species_code: str, index_df: pd.DataFrame, data_dir:str, cols: str, outfile: str
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
    data_df["age"] = data_df["AgeAgree"]
    data_df.columns = data_df.columns.str.lower()
    data_df = data_df[cols]

    # Write data
    outfile = join_path(out_dir, outfile)
    data_df.to_csv(outfile, index=False)

    source = extract_val("source")
    outfile = join_path(out_dir, "README.md")
    with open(outfile, "w+") as f:
        f.writelines(source)


@hydra.main(version_base=None, config_path="conf", config_name="preprocess")
def main(config: DictConfig) -> None:
    """
    The main entry point for the preprocess pipeline.

    Args:
        config (DictConfig): 
            The pipeline configuration.
    """
    # Constants
    data_config = config["data"]
    DATA_DIR = data_config["dir"]
    INDEX = data_config["index"]
    SPECIES_LIST = data_config["species"]
    COLS = data_config["cols"]
    OUTFILE = data_config["out"]

    # Load data
    index_file = join_path(DATA_DIR, INDEX)
    index_df = pd.read_csv(index_file)

    for species_code in SPECIES_LIST:
        write_species_csv(species_code, index_df, DATA_DIR, COLS, OUTFILE)


if __name__ == "__main__":
    main()
