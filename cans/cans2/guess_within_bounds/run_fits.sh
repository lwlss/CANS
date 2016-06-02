#!/bin/bash

# Run multiple scripts in background and pass an arguement to index a
# set inital guesses of kn and C_0. Run using bash run_fits.sh &.
for vals in {1..100}
do
    python fit_real_zone.py $vals &
done
