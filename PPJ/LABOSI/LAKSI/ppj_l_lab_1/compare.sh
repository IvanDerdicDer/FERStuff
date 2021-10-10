#!/bin/bash

for i in {01..29}
do
	echo "Testing $i"
	python3.10 LeksickiAnalizator.py < tests/$i*/test.in | diff tests/$i*/test.out -
done
