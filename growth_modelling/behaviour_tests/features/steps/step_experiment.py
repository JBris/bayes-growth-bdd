######################################
# Imports
######################################

# External
from behave.runner import Context
from behave import given

######################################
# Functions
######################################

def get_context_text(context: Context) -> str:
    """
    Get the cleaned multi-line text from the test context.

    Args:
        context (Context): 
            The test context.

    Returns:
        str: The multi-line text from the test context.
    """
    context_test = (
        str(context.text)
        .replace("\n", " ")
        .replace("\r", "")
        .replace("\\", "")
    )
    return context_test

######################################
# Steps
######################################

@given('that our statement is')
def step_impl(context: Context) -> None:
    context.behaviour.experiment.statement = get_context_text(context)

@given('that our hypothesis is')
def step_impl(context: Context) -> None:
    context.behaviour.experiment.hypothesis = get_context_text(context)

@given('that our aim is to')
def step_impl(context: Context) -> None:
    context.behaviour.experiment.aim = get_context_text(context)