#!/bin/bash

for i in {01..20}
do
	echo "Testing $i"
	python3 Parser.py < testExamples/test$i/test.in | diff testExamples/test$i/test.out -
done
