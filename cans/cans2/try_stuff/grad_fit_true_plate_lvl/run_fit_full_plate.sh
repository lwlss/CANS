#!/bin/bash

for i in {0..4}
do
    python compare_guessed_and_uniform.py $i 0 >/dev/null 2>&1 &
    # python compare_guessed_and_uniform.py $i 1 >/dev/null 2>&1 &
    # python fit_full_plate.py $i >/dev/null &
done
