#!/bin/bash

echo $1 "$2"

a=$(find -wholename "$1/*" | grep -iE "$2")

wc -l $a | grep total