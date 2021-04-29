#!/bin/bash

for i in {01..25}
do
	echo "Testing $i"
	python3 SimPa.py < testExamples/test$i/primjer.in | diff testExamples/test$i/primjer.out -
done
