open $file, $ARGV[0] or die "Cant open file: $ARGV[0]";

@lines = <$file>;
chomp(@lines);

foreach(@lines){
    $_ =~ s/\s//mg;
    $_ =~ s/-/0/mg;
    next if ($_ =~ m/^#/);
    next if ($_ eq "");
    push(@lines1, $_);
}

@multi = split(';', shift(@lines1));

foreach(@lines1){
    @to_append = ();
    @line_s = split(';', $_);
    push(@to_append, shift(@line_s));
    push(@to_append, shift(@line_s));
    push(@to_append, shift(@line_s));

    $sum = 0;

    for $i (0..6){
        $sum += $multi[$i] * $line_s[$i];
    }

    push(@to_append, $sum);
    push(@summed, [@to_append]);
}

@summed = sort { $b->[3] <=> $a->[3] } @summed;

print "Lista po rangu: \n";
print "-----------------\n";

for($i = 0; $i <= $#summed; $i++){
    $row = $i + 1;
    print "$row. $summed[$i]->[1], $summed[$i]->[2] ($summed[$i]->[0]): $summed[$i]->[3]\n";
}

close $file;
