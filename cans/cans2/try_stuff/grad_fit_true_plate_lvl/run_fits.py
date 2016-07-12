#!/bin/bash

for i in {0..4}
do
    for j in {0..1}
    do
	# echo "$i$j"
	python compare_guessed_and_uniform_b.py $i $j >/dev/null 2>&1 &
    done
done
