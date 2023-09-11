######################################
# Imports
######################################

# External
from behave.model import Scenario
from behave.runner import Context

# Internal
from steps.data_model import BehaviourTestModel

######################################
# Functions
######################################


def before_scenario(context: Context, scenario: Scenario) -> None:
    """
    Before scenario environmental control.

    Args:
        context (Context):
            The current test context.
        scenario (Scenario):
            The current test scenario.
    """
    tags = scenario.tags
    fisheries_modelling_tag = "fisheries_modelling"

    if fisheries_modelling_tag in tags:
        context.behaviour = BehaviourTestModel()


def after_feature(context, feature):
    pass
