#!/bin/bash

folderpath=$1

if [ ! -d $folderpath ]
then
    echo "Given folder does not exist"
    echo "Usage: $0 folderpath"
    exit 65
fi

cd ./$folderpath

for i in {01..12}
do
    images=(????"$i"*.jpg)
    images=($(sort <<< ${images[@]}))

    echo "$i :"
    echo "----------"
    
    images_len=${#images[@]}
    for j in `seq 1 $images_len`
    do
        let index=j-1
        echo "  $j. ${images[index]}"
    done
    echo "--- Ukupno: ${images_len} slika ---"
done