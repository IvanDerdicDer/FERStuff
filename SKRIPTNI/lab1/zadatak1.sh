#!/bin/bash

proba="Ovo je proba"

echo $proba

lista_datoteka=("$PWD"/*)

echo ${lista_datoteka[*]}

proba3=""
for i in {1..3}; do
    proba3+="${proba}. "
done

echo $proba3

a=4
b=3
c=7
let d=(a+4)*b%c

echo $a $b $c $d

words=$(wc -w *.txt | grep total)
IFS=' '

read -ra word_count <<< "$words"

echo ${word_count[0]}

ls ~