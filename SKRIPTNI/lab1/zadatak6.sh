#!/bin/bash

if [ ! -d $1 ]
then
    echo "Folder $1 does not exist"
    echo "Usage: $0 folderpath1 folderpath2"
    exit 65
fi

if [ ! -d $2 ]
then
    echo "Folder $2 does not exist"
    echo "Usage: $0 folderpath1 folderpath2"
    exit 65
fi

folderpath1=$1
folderpath2=$2

for file in $folderpath1/*
do
    r=$IFS
    IFS='/'
    read -ra split <<< "$file"
    IFS=$r

    length=${#split[@]}
    let length-=1

    filename=${split[length]}

    if [ ! -f $folderpath2/$filename ]
    then
        echo "$file --> $folderpath2"
        continue
    fi

    if [ $file -nt $folderpath2/$filename ]
    then
        echo "$file --> $folderpath2"
        continue
    fi
done

for file in $folderpath2/*
do
    r=$IFS
    IFS='/'
    read -ra split <<< "$file"
    IFS=$r

    length=${#split[@]}
    let length-=1

    filename=${split[length]}

    if [ ! -f $folderpath1/$filename ]
    then
        echo "$file --> $folderpath1"
        continue
    fi

    if [ $file -nt $folderpath1/$filename ]
    then
        echo "$file --> $folderpath1"
        continue
    fi
done