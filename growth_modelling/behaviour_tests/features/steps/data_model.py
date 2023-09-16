######################################
# Imports
######################################

# External
from abc import ABC
from dataclasses import dataclass, field
from os.path import join as join_path
from pathlib import Path
import yaml

######################################
# Classes
######################################


class BaseDataModel(ABC):
    """Abstract class for data models."""

    def to_dict(self) -> dict:
        """
        Convert data model to dictionary.

        Returns:
            dict: The dictionary of the data model.
        """
        return vars(self)

    def to_yaml(self, out_dir: str, outfile: str = "meta.yaml", default_flow_style: bool = False) -> str:
        """
        Convert the data model to YAML, and write to file.

        Args:
            out_dir (str):
                The output directory.
            outfile (str): 
                The YAML output file.
            default_flow_style (bool, optional): 
                The YAML flow style. Defaults to False.

        Returns:
            str: 
                The YAML file path.
        """
        model_dict = self.to_dict()

        outfile = join_path(out_dir, outfile)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        with open(outfile, 'w') as f:
            yaml.dump(model_dict, f, default_flow_style = default_flow_style)
        return outfile
    
@dataclass
class BayesianModel(BaseDataModel):
    """Class for Bayesian Model parameters."""
    def __init__(self) -> None: 
        self.model_type: str = "linear"
        self.likelihood: str = "gaussian"
        self.sampler_longname: str = "No U-Turn Sampler"
        self.sampler: str = "nuts"
        self.n_draws: int = 2000
        self.n_burn: int = 1000
        self.acceptance_prob: float = 0.8
        self.n_chains: int = 1
        self.parallelisation: bool = True
        self.hdi_prob: float = 0.95
        self.priors: dict = {}
        self.factors: list[str] = []

@dataclass
class FisheriesModel(BaseDataModel):
    """Class for Fisheries Model parameters."""

    def __init__(self) -> None: 
        self.class_type: str = "chondrichthyes"
        self.order: str = "carcharhiniformes"
        self.family: str = "carcharhinidae"
        self.species: str = "carcharhinus_limbatus"
        self.data_source: str = ""
        self.sex: str = "female"
        self.locations: list[str] = []
        self.years: list[int] = []
        self.response_var: str = "fl"
        self.response_unit: str = "cm"
        self.explanatory_var: str = "age"
        self.explanatory_unit: str = "years"
        self.growth_curve: str = "linear"
        self.growth_curve_longname: str = "linear"
    
@dataclass
class BehaviourTestModel(BaseDataModel):
    """Class for behaviour testing parameters."""

    def __init__(self) -> None: 
        self.bayesian: BayesianModel = BayesianModel()
        self.fisheries: FisheriesModel = FisheriesModel()
        self.data_dir: str = join_path("..", "data") 
        self.data_file: str = "data.csv"
        self.random_seed: int = 100
    
    def to_dict(self) -> dict:
        """
        Convert data model to dictionary.

        Returns:
            dict: The dictionary of the data model.
        """
        model_dict = vars(self)
        for k in model_dict:
            if not hasattr(model_dict[k], '__dict__'):
                continue
            model_dict[k] = vars(model_dict[k])
        return model_dict