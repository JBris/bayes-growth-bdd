#!/usr/bin/env bash

. .env

###################################################################
# Constants
###################################################################

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export MLFLOW_S3_ENDPOINT_URL=$MLFLOW_S3_ENDPOINT_URL

OUT_DIR=data/chondrichthyes/carcharhiniformes

###################################################################
# Main
###################################################################

cd growth_modelling

dvc stage add --force -n preprocess \
    -d src/preprocess.py -d data/limbatus.csv -d data/spot_tail_shark.csv -d conf/config.yaml \
    -d conf/common/carcharhiniformes.yaml -d conf/preprocess/carcharhiniformes.yaml \
    -o ${OUT_DIR}/carcharhinus_limbatus/data.csv -o ${OUT_DIR}/carcharhinus_tilstoni/data.csv \
    -o ${OUT_DIR}/carcharhinus_sorrah/data.csv -o ${OUT_DIR}/carcharhinus_limbatus/README.md \
    -o ${OUT_DIR}/carcharhinus_tilstoni/README.md  -o ${OUT_DIR}/carcharhinus_sorrah/README.md \
    python src/preprocess.py
    
dvc stage add --force -n plot_curves \
    -d src/plot_curves.py -d ${OUT_DIR}/carcharhinus_limbatus/data.csv -d ${OUT_DIR}/carcharhinus_tilstoni/data.csv \
    -d ${OUT_DIR}/carcharhinus_sorrah/data.csv -d conf/config.yaml -d conf/experiment_tracking/local.yaml \
    -d conf/common/carcharhiniformes.yaml -d conf/plot/carcharhiniformes.yaml \
    -o ${OUT_DIR}/carcharhinus_limbatus/fl_age.png  -o ${OUT_DIR}/carcharhinus_tilstoni/fl_age.png \
    -o ${OUT_DIR}/carcharhinus_sorrah/fl_age.png \
    python src/plot_curves.py

dvc repro