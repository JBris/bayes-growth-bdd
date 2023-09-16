#!/usr/bin/env bash

. .env

###################################################################
# Constants
###################################################################

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export MLFLOW_S3_ENDPOINT_URL=$MLFLOW_S3_ENDPOINT_URL

###################################################################
# Main
###################################################################

cd growth_modelling/behaviour_tests

behave --tags carcharhinus_tilstoni,carcharhinus_limbatus,carcharhinus_sorrah --show-timings --junit
