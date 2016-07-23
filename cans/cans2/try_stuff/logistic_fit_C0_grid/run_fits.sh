#!/bin/bash

for i in {0..49}
do
    python fit_logistic.py $i >/dev/null 2>&1 &
done
