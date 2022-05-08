use open ':locale';
use locale;

$prefix_len = '*';

if($#ARGV + 1 > 1){
    $prefix_len = pop(@ARGV) * 1;
    foreach(@ARGV){
        open $file, $_ or die "Cant open file: $_";

        @lines = <$file>;

        $words = "";

        foreach $i (@lines){
            $i =~ s/\n+/ /mg;
            $i =~ s/[[:punct:]]//mg;
            $words .= $i;
        }

    	@words = split(' ', $words);

        %prefix_match = ();

        foreach $i (@words){
            next if(length $i < $prefix_len);
            $i = lc $i;
            $i =~ m/[[:alpha:]]{$prefix_len}/;
            $prefix_match{$&} += 1;
        }

        foreach $i (sort keys %prefix_match){
            print "$i : $prefix_match{$i}\n";
        }

        close $file;
    }
}else{
    @lines = <>;

    $words = "";

    foreach $i (@lines){
        $i =~ s/\s+/ /mg;
        $i =~ s/[[:punct:]]//mg;
        $words .= $i;
    }

    @words = split(' ', $words);

    %prefix_match = ();

    foreach $i (@words){
        next if(length $i < $prefix_len);
        $i = lc $i;
        $i =~ m/[[:alpha:]]+/;
        $prefix_match{$&} += 1;
    }

    foreach $i (sort keys %prefix_match){
        print "$i : $prefix_match{$i}\n";
    }
}