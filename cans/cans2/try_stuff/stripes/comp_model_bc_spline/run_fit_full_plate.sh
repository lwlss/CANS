#!/bin/bash

# C_ratio
for i in {0..9}
do
    # Stripes or filled plate
    for j in {0..1}
    do
	# Slicing of b_values
	for k in {0..1}
	do
	    python fit_full_plate.py $i $j $k >/dev/null 2>&1 &
	done
    done
done
