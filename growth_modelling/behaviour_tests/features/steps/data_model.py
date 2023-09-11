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

    def to_yaml(self, out_dir: str, outfile: str = "config.yaml", default_flow_style: bool = False) -> str:
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

    model_type: str = "linear"
    likelihood: str = "gaussian"
    sampler_longname: str = "No U-Turn Sampler"
    sampler: str = "nuts"
    n_draws: int = 2000
    n_burn: int = 1000
    acceptance_prob: float = 0.8
    n_chains: int = 1
    parallelisation: bool = True
    hdi_prob: float = 0.95
    priors: dict = field(default_factory=dict)  

@dataclass
class FisheriesModel(BaseDataModel):
    """Class for Fisheries Model parameters."""

    class_: str = "chondrichthyes"
    order: str = "carcharhiniformes"
    family: str = "carcharhinidae"
    species: str = "carcharhinus_limbatus"
    data_source: str = ""
    sex: str = "female"
    locations: list[str] = field(default_factory=list)
    years: list[int] = field(default_factory=list)
    response_var: str = "fl"
    response_unit: str = "cm"
    explanatory_var: str = "age"
    explanatory_unit: str = "years"

@dataclass
class BehaviourTestModel(BaseDataModel):
    """Class for behaviour testing parameters."""

    bayesian: BayesianModel = BayesianModel()
    fisheries: FisheriesModel = FisheriesModel()
    data_dir: str = join_path("..", "data") 
    data_file: str = "data.csv"
    random_seed: int = 100
    
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