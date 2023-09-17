@carcharhinus_tilstoni
Feature: Linear growth model for Australian blacktip sharks (Carcharhinus tilstoni)
    Background:
        Given we are fitting a "linear" Bayesian multilevel growth model using "No U-Turn Sampler" ("NUTS")
        And we are fitting a growth model with a "Gaussian" likelihood
        And we are running "4" Markov chain Monte Carlo (MCMC) chains with parallelisation "enabled"
        And we are taking "2000" draws per MCMC chain
        And we specify "2000" samples for our burn-in period
        And our MCMC samples have an acceptance probability of "0.999"
        And our class is "Chondrichthyes"
        And our order is "Carcharhiniformes"
        And our family is "Carcharhinidae"
        And our species is "Carcharhinus tilstoni"
        And our data source is "Harry et al. (2019)"
        And we set our random seed to "100"

    @fisheries_modelling
    Scenario: Fit a linear model for male Australian blacktip sharks (Carcharhinus tilstoni)
        When our sex is "Male"
        And we have samples taken from "New South Wales A, and Queensland A"
        And we have samples taken between "2007" and "2012"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "intercept" parameter could plausibly be "55.0" with a standard deviation of "10.0"
        And we believe that the "slope" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.05"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.035"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"
        And we expect the posterior mean of the "intercept" parameter estimate to be "55.0" with "0.05" error
        And we expect the posterior mean of the "slope" parameter estimate to be "6.0" with "0.25" error
        And we expect the posterior mean of the "sigma" parameter estimate to be "6.0" with "0.25" error

    @fisheries_modelling
    Scenario: Fit a linear model for female Australian blacktip sharks (Carcharhinus tilstoni)
        When our sex is "Female"
        And we have samples taken from "New South Wales A, and Queensland A"
        And we have samples taken between "2007" and "2012"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "intercept" parameter could plausibly be "55.0" with a standard deviation of "10.0"
        And we believe that the "slope" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.05"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.035"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"
        And we expect the posterior mean of the "intercept" parameter estimate to be "54.0" with "0.05" error
        And we expect the posterior mean of the "slope" parameter estimate to be "6.0" with "0.25" error
        And we expect the posterior mean of the "sigma" parameter estimate to be "6.0" with "0.25" error