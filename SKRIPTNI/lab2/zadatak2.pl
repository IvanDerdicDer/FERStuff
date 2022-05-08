print "Enter numbers > ";
$numbers = <>;

chomp($numbers);

@arr = split(' ', $numbers);

$len = @arr;

$sum += $_ for @arr;

print $sum / $len;
