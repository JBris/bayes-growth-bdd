#!/usr/bin/env bash

OUT_DIR=data/chondrichthyes/carcharhiniformes

cd growth_modelling

dvc stage add --force -n preprocess \
    -d src/preprocess.py -d data/limbatus.csv -d data/spot_tail_shark.csv -d src/growth_lib -d src/conf/preprocess.yaml \
    -o ${OUT_DIR}/carcharhinus_limbatus/data.csv -o ${OUT_DIR}/carcharhinus_tilstoni/data.csv \
    -o ${OUT_DIR}/carcharhinus_sorrah/data.csv -o ${OUT_DIR}/carcharhinus_limbatus/README.md \
    -o ${OUT_DIR}/carcharhinus_tilstoni/README.md  -o ${OUT_DIR}/carcharhinus_sorrah/README.md \
    python src/preprocess.py data.species=[btp,abt,sss] data.out=data.csv
    