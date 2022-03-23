#!/bin/bash

grep -iE "banana|jabuka|jagoda|dinja|lubenica" namirnice.txt

grep -ivE "banana|jabuka|jagoda|dinja|lubenica" namirnice.txt

grep -rnE " [A-Z]{3}[0-9]{6} *|$" ~/projekti/

find . -mtime 7 -mtime -14 -daystart -ls

for ia in {1..15}; do echo $ia; done

kraj=15

for ia in {1..$kraj}; do echo $ia; done

for ia in $(eval echo "{1..$kraj}"); do echo $ia; done

for ia in $(seq 1 $kraj); do echo $ia; done