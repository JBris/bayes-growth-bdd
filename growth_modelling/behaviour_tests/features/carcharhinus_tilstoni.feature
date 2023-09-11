@carcharhinus_tilstoni
Feature: Growth model for Carcharhinus tilstoni
    Background:
        Given we are fitting a "linear" Bayesian multilevel model using "No U-Turn Sampler" ("NUTS")
        And we are running "4" Markov chain Monte Carlo (MCMC) chains with parallelisation "enabled"
        And we are taking "10" draws per MCMC chain
        And we specify "5" samples for our burn-in period
        And our MCMC samples have an acceptance probability of "0.8"
        And our class is "Chondrichthyes"
        And our order is "Carcharhiniformes"
        And our species is "Carcharhinus tilstoni"
        And our data source is "Harry et al. (2019)"

    @fisheries_modelling
    Scenario: Fit a growth model for male sharks
        When our sex is "Male"
        And we have samples taken from "New South Wales A, and Queensland A"
        And we have samples taken between "2007" and "2012"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we retrieve our data from "data.csv"
        And we fit our Bayesian multilevel model

