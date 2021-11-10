#!/bin/bash

for i in {01..30}
do
	echo "Testing $i"
	python3.10 SintaksniAnalizator.py < tests/$i*/test.in | diff tests/$i*/test.out -
done
