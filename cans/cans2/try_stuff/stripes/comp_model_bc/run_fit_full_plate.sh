#!/bin/bash

for i in {0..9}
do
    python fit_full_plate.py $i >/dev/null 2>&1 &
    # python fit_full_plate.py $i >/dev/null &
done
