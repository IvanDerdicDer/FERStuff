if($#ARGV + 1 > 0){    
    foreach(@ARGV){
        $_ =~ m/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/;
        open $file, $_ or die "Cant open file: $_";
        print "Datum: $&\n";
        print "sat : broj pristupa\n";
        print "---------------\n";
        while($line = <$file>){
            $line =~ m/:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/;
            @time = split(':', $&);
            $hours = $time[1] * 1;
            $count_arr[$hours] += 1;
        }
        foreach(00..23){
            print "$_ : $count_arr[$_]\n";
        }
        close $file;
    }
}else{
    print "sat : broj pristupa\n";
    print "---------------\n";
    while($line = <>){
        $line =~ m/:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/;
        @time = split(':', $&);
        $hours = $time[1] * 1;
        $count_arr[$hours] += 1;
    }
    foreach(00..23){
            print "$_ : $count_arr[$_]\n";
        }
}