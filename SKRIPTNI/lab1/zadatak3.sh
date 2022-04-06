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
	#temp1=`cat $file | cut -d '"' -f 2 | sort | uniq -c | sort -nr | sed -r 's/\s{4}([\s0-9]+)\s+(.*)/  \1 : \2/'`
	cat $file | cut -d '"' -f 2 | sort | uniq -c | sort -nr | sed -r 's/\s{,4}([\s0-9]+)\s+(.*)/  \1 : \2/'
	#echo $temp1
	#temp2=` sort $temp1| uniq -c` 
	#echo $temp1 | sort -nr | sed -r 's/\s{4}([\s0-9]+)\s+(.*)/  \1 : \2/'
	echo
done
