@carcharhinus_tilstoni
Feature: Growth model for Carcharhinus tilstoni
    Background:
        Given we are fitting a "linear" Bayesian multilevel model using "No U-Turn Sampler" ("NUTS")
        And we are fitting a model with a "Gaussian" likelihood
        And we are running "4" Markov chain Monte Carlo (MCMC) chains with parallelisation "enabled"
        And we are taking "100" draws per MCMC chain
        And we specify "100" samples for our burn-in period
        And our MCMC samples have an acceptance probability of "0.8"
        And our class is "Chondrichthyes"
        And our order is "Carcharhiniformes"
        And our species is "Carcharhinus tilstoni"
        And our data source is "Harry et al. (2019)"
        And we set our random seed to "100"

    @fisheries_modelling
    Scenario: Fit a growth model for male sharks
        When our sex is "Male"
        And we have samples taken from "New South Wales A, and Queensland A"
        And we have samples taken between "2007" and "2012"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "intercept" parameter could plausibly be "55.0" with a standard deviation of "10.0"
        And we believe that the "slope" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model, then evaluate its "0.95" highest density intervals (HDIs)
        Then we expect our "Effective sample size" ("ESS bulk") diagnostic to be at "greater than" "1.0"