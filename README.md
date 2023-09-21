# Bayes Growth BDD

[![Validate Pipeline](https://github.com/JBris/bayes-growth-bdd/actions/workflows/validation.yml/badge.svg)](https://github.com/JBris/bayes-growth-bdd/actions/workflows/validation.yml) [![Documentation](https://github.com/JBris/bayes-growth-bdd/actions/workflows/docs.yml/badge.svg)](https://github.com/JBris/bayes-growth-bdd/actions/workflows/docs.yml) [![pages-build-deployment](https://github.com/JBris/bayes-growth-bdd/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/JBris/bayes-growth-bdd/actions/workflows/pages/pages-build-deployment)

Website: [Bayes Growth BDD](https://jbris.github.io/bayes-growth-bdd/)

*Demonstrating the use of behavior-driven development (BDD) for monophasic and biphasic Bayesian fisheries growth models on sharks.*

# Table of contents

- [Bayes Growth BDD](#bayes-growth-bdd)
- [Table of contents](#table-of-contents)
  - [Project](#project)
    - [Overview](#overview)
    - [Python Environment](#python-environment)
      - [PyMC](#pymc)
      - [behave](#behave)
    - [Data](#data)
      - [Background](#background)
      - [Navigation](#navigation)
    - [Experiment tracking](#experiment-tracking)
    - [Discussion](#discussion)
  - [Background and theory](#background-and-theory)
    - [Biphasic growth](#biphasic-growth)
  - [References](#references)

## Project

### Overview

The general idea behind this demonstration is to synthesise the behavior-driven development (BDD) testing approach that is more commonly used within *agile* software development with Bayesian statistical modelling. With a marine biology flavour. The overall aim is to demonstrate how BDD can enable and faciliate communication among different disciplines using a common human-readable language. This is particularly important within highly technical scientific domains where cross-disciplinary communication may be more challenging. 

BDD was chosen as it (at least in theory) faciliates collaboration and communication within multidisciplinary projects. Namely, it encourages business analysts and developers to collaborate in specifying the behaviour of software, via the use of user stories. These user stories should be written to a formal document. For this demonstration, these documents are written in the popular Gherkin syntax.

Likewise, by using a Bayesian modelling approach, we can easily incorporate prior assumptions from domain experts (marine biologists in this case) into our models. These assumptions can be documented in Gherkin, and would be recorded by business analysts as user stories. 

### Python Environment

[Python dependencies are specified in this requirements.txt file.](services/python/requirements.txt) It's recommended that you create a virtual environment before installing these dependencies.

#### PyMC

[The PyMC library was used to specify all Bayesian growth models.](https://www.pymc.io/welcome.html) This demonstration specifically implements nonlinear, Bayesian multilevel models using PyMC. 

Documentation for actually implementing nonlinear, Bayesian multilevel models with multiple factors using PyMC is pretty limited. I probably should have used Stan instead :sunglasses:

#### behave

[The behave package was used to implement all BDD tests.](https://behave.readthedocs.io/en/stable/index.html). These tests have been written using Gherkin syntax. [For more information on Gherkin, click here.](https://cucumber.io/docs/gherkin/reference/)

* [Feature files containing human-readable Gherkin can be found here.](growth_modelling/behaviour_tests/features) 
* [The implementation of the scenario steps can be found here.](growth_modelling/behaviour_tests/features/steps/) 

### Data

#### Background

Publicly available age and growth data for the following species were included in this demonstration:

* Blacktip shark (*Carcharhinus limbatus*)
* Spot-tail shark (*Carcharhinus sorrah*)
* Australian blacktip shark (*Carcharhinus tilstoni*)

All data used in this demonstration were retrieved from the following sources:

* https://github.com/alharry/limbatus/tree/master/data
* https://github.com/alharry/spot-tail

With the respective citations:

* Harry, A. V., Butcher, P. A., Macbeth, W. G., Morgan, J. A., Taylor, S. M., & Geraghty, P. T. (2019). Life history of the common blacktip shark, Carcharhinus limbatus, from central eastern Australia and comparative demography of a cryptic shark complex. Marine and Freshwater Research, 70(6), 834-848.
* Harry, A. V., Tobin, A. J., & Simpfendorfer, C. A. (2013). Age, growth and reproductive biology of the spot-tail shark, Carcharhinus sorrah, and the Australian blacktip shark, C. tilstoni, from the Great Barrier Reef World Heritage Area, north-eastern Australia. Marine and freshwater research, 64(4), 277-293.

#### Navigation

* [The unprocessed data can be found by here.](growth_modelling/data/)
* [The processed data can be found by here.](growth_modelling/data/chondrichthyes/carcharhiniformes/)
* [This DVC pipeline can be executed to reproduce the data processing steps.](scripts/preprocess_data.sh)
* [The Hydra configuration files for the DVC pipeline can be found here.](growth_modelling/conf/)
* [The BDD test results can be found here.](growth_modelling/behaviour_tests/out/chondrichthyes/carcharhiniformes/)

### Experiment tracking

* [An optional Docker configuration has been provided to facilitate experiment tracking.](docker-compose.yml)
* [See the .env file for Docker environment variables.](.env)
* [The docker_up.sh script can be executed to launch the Docker services.](scripts/docker_up.sh)
* [MLFlow is available for experiment tracking.](https://mlflow.org/)
* [Also, MinIO is available for storing experiment artifacts.](https://min.io/)

Experiment tracking is currently not being heavily used within the demonstration, but the option is definitely there... 

### Discussion

[The Gherkin documents here describe a statistical modelling exercise applied to 3 species of shark to evaluate and compare monophasic and biphasic Bayesian growth models.](growth_modelling/behaviour_tests/features) From statistical evidence provided by previous works on the subject, there is some reason to believe that biphasic models typically offer a superior statistical fit. For initial reading, refer to:

* Araya, M., & Cubillos, L. A. (2006). Evidence of two-phase growth in elasmobranchs. Environmental Biology of Fishes, 77, 293-300.
* Wilson, K. L., Honsey, A. E., Moe, B., & Venturelli, P. (2018). Growing the biphasic framework: Techniques and recommendations for fitting emerging growth models. Methods in Ecology and Evolution, 9(4), 822-833.

[Using spot-tail sharks as an example, we compared a monophasic and biphasic von Bertalanffy growth model (VBGM) for each sex. In the Gherkin document, we have recorded the specification of the Bayesian growth model, baseline diagnostic values, our expected results, and various types of metadata.](growth_modelling/behaviour_tests/features/carcharhinus_sorrah.feature) 

[The metadata is outputted as a YAML file, which we can save using experiment tracking and use to replicate our experiments.](growth_modelling/behaviour_tests/out/chondrichthyes/carcharhiniformes/carcharhinus_sorrah/m/nonlinear/vbgm/meta.yaml)

Notably, the results of the modelling exercise were fairly mixed - meaning that the biphasic growth models did not consistently outperform the monophasic growth models. 

## Background and theory

The growth function most commonly used within fisheries science to model growth patterns and length-at-age relationships is the von Bertalanffy growth model (VBGM) [[1]](#1). The VBGM provides informative parameter estimates including growth rates and maximum lengths [[1]](#1). The familiar Beverton-Holt parameterisation [[2]](#2) of the VBGM is as follows:

$$
L(t) = L_\infty (1 - e^{-k(t - t_0)})
$$ 

where $L(t)$ is the length as a function of time; $L_\infty$ is the asymptotic length-at-age (cm); $k$ is the Brody growth coefficient (per year) determining the rate at which the fish will reach the asymptotic length-at-age; and $t_0$ is the theoretical time at length zero. 

Though the VBGM is highly popular, the assumption that a monophasic curve can model the entire lifetime growth of chondrichthyans has received criticism. For instance, a single curve may fail to account for changes in energy reallocation and growth that occur at the onset of maturity, resulting in models that fit poorly to the smallest or largest of individuals [[3]](#3). Therefore, a biphasic growth model may better characterise growth patterns for both the juvenile and mature life stages of chondrichthyans [[4]](#4), potentially leading to more robust parameter estimates of growth. More accurate parameter estimates typically lead to more accurate stock assessments, and help to inform both conservation and fisheries management [[5]](#5). Hence, robust length-at-age models are key to the effective management and sustainability of fisheries.

### Biphasic growth

In contrast to teleostei, reproductive investment is relatively high for most chondrichthyans, so any changes in somatic growth rates following the age-at-maturity are more likely to be identified from growth and age data alone [[6]](#6). One contributing factor to these changes in growth rates is energy reallocation away from somatic growth and towards reproductive investment [[4]](#4).

Soriano et al.'s [[7]](#7) biphasic modifications to the common VBGM, hereafter referred to as the biphasic VBGM (BVBGM), have been applied to a number of chondrichthyes within several age and growth studies. For instance, Acuna et al. [[8]](#8) made use of the BVBGM to model the growth of three pelagic sharks: *Lamna nasus*, *Isurus oxyrinchus*, *Prionace glauca*. 

Soriano et al. [[7]](#7) proposed two continuous modifications to the common VBGM. For each, a new factor $A(t)$ is proposed:

$$
A(t) = 1 - \frac{h}{1 + (t - t_h)^2 }
$$  

where $t_h$ is the age in which the phasic shift occurs; and $h$ is the magnitude of the maximum difference in length-at-age between the common VBGM and the BVBGM. For the purposes of this demonstration, we use form *A* of Soriano et al.'s [[7]](#7) BVBGM:

$$
L(t) = L_\infty A(t) (1 - e^{-k(t - t_0)})
$$

where $A(t)$ modifies $L_\infty$ as age increases.

## References

<a id="1">[1]</a> Ricker, W. E. (1975). Computation and interpretation of biological statistics of fish populations. Fish. Res. Board Can. Bull., 191, 1-382.

<a id="2">[2]</a> Beverton, R. J. H., & Holt, S. J. (1957). On the dynamics of exploited fish populations.

<a id="3">[3]</a> Quince, C., Shuter, B. J., Abrams, P. A., & Lester, N. P. (2008). Biphasic growth in fish II: empirical assessment. Journal of Theoretical Biology, 254(2), 207-214.

<a id="4">[4]</a> Araya, M., & Cubillos, L. A. (2006). Evidence of two-phase growth in elasmobranchs. Environmental Biology of Fishes, 77, 293-300.

<a id="5">[5]</a> Pardo, S. A., Cooper, A. B., & Dulvy, N. K. (2013). Avoiding fishy growth curves. Methods in Ecology and Evolution, 4(4), 353-360.

<a id="6">[6]</a> Frisk, M. G., Miller, T. J., & Fogarty, M. J. (2001). Estimation and analysis of biological parameters in elasmobranch fishes: a comparative life history study. Canadian Journal of Fisheries and Aquatic Sciences, 58(5), 969-981.

<a id="7">[7]</a> Soriano, M., Moreau, J., Hoenig, J. M., & Pauly, D. (1992). New functions for the analysis of two-phase growth of juvenile and adult fishes, with application to Nile perch. Transactions of the American Fisheries Society, 121(4), 486-493.

<a id="8">[8]</a> Acuña, E., Cid, L., Pérez, E., Kong, I., Araya, M., Lamilla, J., ... & Barraza, O. (2001). Estudio biológico de tiburones (marrajo dentudo, azulejo y tiburón sardinero) en la zona norte y central de Chile. Informe final, Proyecto FIP, (2000-23), 112.
