#!/bin/bash

for i in {01..14}
do
	echo "Testing $i"
	python3 MinDka.py < testExamples/test$i/t.ul | diff testExamples/test$i/t.iz -
done
