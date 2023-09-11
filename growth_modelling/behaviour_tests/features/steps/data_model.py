######################################
# Imports
######################################

# External
from abc import ABC
from dataclasses import dataclass, field
from os.path import join as join_path

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


@dataclass
class BayesianModel(BaseDataModel):
    """Class for Bayesian Model parameters."""

    model_type: str = "linear"
    sampler_longname: str = "No U-Turn Sampler"
    sampler: str = "nuts"
    n_draws: int = 2000
    n_burn: int = 1000
    acceptance_prob: float = 0.8
    n_chains: int = 1
    parallelisation: bool = True


@dataclass
class FisheriesModel(BaseDataModel):
    """Class for Fisheries Model parameters."""

    class_: str = "chondrichthyes"
    order: str = "carcharhiniformes"
    species: str = "carcharhinus_limbatus"
    data_source: str = ""
    sex: str = "female"
    locations: list[str] = field(default_factory=list)
    years: tuple[int] = field(default_factory=tuple)
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
    
    def to_dict(self) -> dict:
        """
        Convert data model to dictionary.

        Returns:
            dict: The dictionary of the data model.
        """
        model_dict = vars(self)
        for k in model_dict:
            model_dict[k] = vars(model_dict[k])
        return model_dict