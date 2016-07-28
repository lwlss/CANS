#!/bin/bash

for i in {0..9}
do
    for j in {0..1}
    do
	python fit_full_plate.py $i $j >/dev/null 2>&1 &
    done
done
