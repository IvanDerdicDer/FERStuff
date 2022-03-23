#!/bin/bash

if [ ! -d $1 ]
then
    echo "Given path does not exist"
    echo "Usage: $0 folderpath"
    exit 65
fi

for file in $(ls $1/*02*.txt); do
	echo "datum: $(echo $file | sed -r 's/[a-z_]*\.([1-9][0-9]{3})-([0-9]{2})-([0-9]{2}).txt/\3-\2-\1/')"
	echo '---------------------------------------------------------------------------------'
	temp1=cat $file | sed '/^[[:space:]]*$/d' | cut -d '"' -f 2 
	temp2=`echo $temp1 | sort | uniq -c` 
	echo $temp2 | sort -nr | sed -r 's/\s{4}([\s0-9]+)\s+(.*)/  \1 : \2/'
	echo
done
