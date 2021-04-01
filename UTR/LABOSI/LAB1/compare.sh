#!/bin/bash

for i in {01..53}
do
	echo "Testing $i"
	python3 SimEnka.py < testExamples2/test$i/test.a | diff testExamples2/test$i/test.b -
done
