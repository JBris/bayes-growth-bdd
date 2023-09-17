######################################
# Imports
######################################

# External
from behave.model import Feature, Scenario
from behave.runner import Context

# Internal
from steps.data_model import BehaviourTestModel

######################################
# Functions
######################################


def before_feature(context: Context, feature: Feature) -> None:
    """
    Before feature environmental control.

    Args:
        context (Context):
            The current test context.
        feature (Feature):
            The current test feature.
    """
    context.traces = {}


def after_feature(context: Context, feature: Feature) -> None:
    """
    After feature environmental control.

    Args:
        context (Context):
            The current test context.
        feature (Feature):
            The current test feature.
    """
    context.traces = None


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
        context.model_scores = {}


def after_scenario(context: Context, scenario: Scenario) -> None:
    """
    After scenario environmental control.

    Args:
        context (Context):
            The current test context.
        scenario (Scenario):
            The current test scenario.
    """
    tags = scenario.tags
    fisheries_modelling_tag = "fisheries_modelling"

    if fisheries_modelling_tag in tags:
        context.behaviour = None
        context.model_scores = None
        