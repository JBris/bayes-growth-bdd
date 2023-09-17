@carcharhinus_sorrah
Feature: Nonlinear growth model for spot-tail sharks (Carcharhinus sorrah)
    Background:
        Given our statement that:
            """
            Energy reallocation from somatic growth to sexual reproduction at the onset of sexual maturity
            contributes to decreases in somatic growth rates following the age-at-maturity
            """
        And our hypothesis that:
            """
            Biphasic growth models will provide a superior statistical fit when compared to monophasic growth models
            as they are able to account for changes in somatic growth rates following the age-at-maturity
            """"
        And we are fitting a "nonlinear" Bayesian multilevel growth model using "No U-Turn Sampler" ("NUTS")
        And we are fitting a growth model with a "Gaussian" likelihood
        And we are running "4" Markov chain Monte Carlo (MCMC) chains with parallelisation "enabled"
        And we are taking "1500" draws per MCMC chain
        And we specify "1500" samples for our burn-in period
        And our MCMC samples have an acceptance probability of "0.99"
        And our class is "Chondrichthyes"
        And our order is "Carcharhiniformes"
        And our family is "Carcharhinidae"
        And our species is "Carcharhinus sorrah"
        And our data source is "Harry et al. (2013)"
        And we set our random seed to "100"

    @fisheries_modelling
    Scenario: Fit a von Bertalanffy growth model for male spot-tail sharks (Carcharhinus sorrah)
        Given our growth curve is a "von Bertalanffy growth model" ("VBGM")
        When our sex is "Male"
        And we have samples taken between "2007" and "2012"
        And recorded location data are unavailable
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "90.0" with a standard deviation of "15.0" and a "lower" bound of "0.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0" and a "lower" bound of "0.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Fit a biphasic von Bertalanffy growth model for male spot-tail sharks (Carcharhinus sorrah)
        Given our growth curve is a "biphasic von Bertalanffy growth model" ("BVBGM")
        When our sex is "Male"
        And we have samples taken between "2007" and "2012"
        And recorded location data are unavailable
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "90.0" with a standard deviation of "15.0" and a "lower" bound of "0.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0" and a "lower" bound of "0.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we believe that the "t_h" parameter could plausibly be "2.5" with a standard deviation of "0.75" and a "lower" bound of "0.0"
        And we believe that the "h" parameter could plausibly be "0.0" with a standard deviation of "1.5" and a "lower" bound of "0.0"
        And we fit random intercepts to "year"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Compare monophasic and biphasic growth models for male spot-tail sharks (Carcharhinus sorrah)
        When our sex is "Male"

    @fisheries_modelling
    Scenario: Fit a von Bertalanffy growth model for female spot-tail sharks (Carcharhinus sorrah)
        Given our growth curve is a "von Bertalanffy growth model" ("VBGM")
        When our sex is "Female"
        And we have samples taken between "2007" and "2012"
        And recorded location data are unavailable
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "110.0" with a standard deviation of "15.0" and a "lower" bound of "0.0"
        And we believe that the "k" parameter could plausibly be "5.0" with a standard deviation of "5.0" and a "lower" bound of "0.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we fit random intercepts to "year"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Fit a biphasic von Bertalanffy growth model for female spot-tail sharks (Carcharhinus sorrah)
        Given our growth curve is a "biphasic von Bertalanffy growth model" ("BVBGM")
        When our sex is "Female"
        And we have samples taken between "2007" and "2012"
        And recorded location data are unavailable
        And our response variable is "Fork Length" ("cm")
        And our explanatory variable is "Age" ("years")
        And we believe that the "L_inf" parameter could plausibly be "110.0" with a standard deviation of "15.0" and a "lower" bound of "0.0"
        And we believe that the "k" parameter could plausibly be "6.0" with a standard deviation of "5.0" and a "lower" bound of "0.0"
        And we believe that the "t_0" parameter could plausibly be "0.0" with a standard deviation of "5.0"
        And we believe that the "t_h" parameter could plausibly be "2.5" with a standard deviation of "0.75" and a "lower" bound of "0.0"
        And we believe that the "h" parameter could plausibly be "0.0" with a standard deviation of "1.5" and a "lower" bound of "0.0"
        And we fit random intercepts to "year"
        And we aim to evaluate the "0.95" highest posterior density intervals (HDIs) of our parameter estimates
        And we retrieve our data from the "data.csv" file
        And we fit our Bayesian model
        Then we expect our "Effective sample size" ("ESS bulk") diagnostics to all be "greater than" "500.0"
        And we expect our "Effective sample size" ("ESS tail") diagnostics to all be "greater than" "500.0"
        And we expect our "Monte carlo standard error" ("MCSE mean") diagnostics to all be "less than" "0.2"
        And we expect our "Monte carlo standard error" ("MCSE sd") diagnostics to all be "less than" "0.2"
        And we expect our "Gelman-Rubin statistic" ("R-hat") diagnostics to all be "less than" "1.1"

    @fisheries_modelling
    Scenario: Compare monophasic and biphasic growth models for female spot-tail sharks (Carcharhinus sorrah)
        When our sex is "Female"