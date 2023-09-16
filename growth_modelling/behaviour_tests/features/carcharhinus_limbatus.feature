@carcharhinus_limbatus
Feature: Nonlinear growth model for blacktip sharks (Carcharhinus limbatus)
    Background:
        Given we are fitting a "nonlinear" Bayesian multilevel growth model using "No U-Turn Sampler" ("NUTS")
        And we are fitting a growth model with a "Gaussian" likelihood
        And we are running "4" Markov chain Monte Carlo (MCMC) chains with parallelisation "enabled"
        And we are taking "1500" draws per MCMC chain
        And we specify "1500" samples for our burn-in period
        And our MCMC samples have an acceptance probability of "0.99"
        And our class is "Chondrichthyes"
        And our order is "Carcharhiniformes"
        And our family is "Carcharhinidae"
        And our species is "Carcharhinus limbatus"
        And our data source is "Harry et al. (2019)"
        And we set our random seed to "100"

    @fisheries_modelling
    Scenario: Fit a von Bertalanffy growth model for male blacktip sharks (Carcharhinus limbatus)
        Given our growth curve is a "von Bertalanffy growth model" ("VBGM")
        When our sex is "Male"
        And we have samples taken from "New South Wales A, New South Wales B, Queensland A, and Queensland B"
        And we have samples taken between "2004" and "2013"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "200.0" with a standard deviation of "20.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Fit a biphasic von Bertalanffy growth model for male blacktip sharks (Carcharhinus limbatus)
        Given our growth curve is a "biphasic von Bertalanffy growth model" ("BVBGM")
        When our sex is "Male"
        And we have samples taken from "New South Wales A, New South Wales B, Queensland A, and Queensland B"
        And we have samples taken between "2004" and "2013"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "200.0" with a standard deviation of "20.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we believe that the "t_h" parameter could plausibly be "4.5" with a standard deviation of "1.0"
        And we believe that the "h" parameter could plausibly be "0.0" with a standard deviation of "2.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Fit a von Bertalanffy growth model for female blacktip sharks (Carcharhinus limbatus)
        Given our growth curve is a "von Bertalanffy growth model" ("VBGM")
        When our sex is "Female"
        And we have samples taken from "New South Wales A, New South Wales B, Queensland A, and Queensland B"
        And we have samples taken between "2004" and "2013"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "220.0" with a standard deviation of "20.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Fit a biphasic von Bertalanffy growth model for female blacktip sharks (Carcharhinus limbatus)
        Given our growth curve is a "biphasic von Bertalanffy growth model" ("BVBGM")
        When our sex is "Female"
        And we have samples taken from "New South Wales A, New South Wales B, Queensland A, and Queensland B"
        And we have samples taken between "2004" and "2013"
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "220.0" with a standard deviation of "20.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we believe that the "t_h" parameter could plausibly be "6.5" with a standard deviation of "1.0"
        And we believe that the "h" parameter could plausibly be "0.0" with a standard deviation of "2.0"
        And we fit random intercepts to "year and location"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"