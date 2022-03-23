#!/bin/bash

echo $(find -name '*.sh')

for i in $(find -name '*.sh')
do
    echo $i
done