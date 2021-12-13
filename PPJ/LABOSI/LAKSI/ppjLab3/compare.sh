#!/bin/bash

for i in {01..19..2}
do
	echo "Testing $i"
	python3.10 SemantickiAnalizator.py < test/$i*/test.in | diff test/$i*/test.out -
done
