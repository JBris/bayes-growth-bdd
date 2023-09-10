#!/usr/bin/env bash

rm -rf docs
cd growth_modelling/docs/
make html
mv build/html/ ../../docs
