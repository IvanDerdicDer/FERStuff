use Time::Piece;
use Time::Seconds;

if($#ARGV + 1 == 1){
    open $file, $ARGV[0] or die "Cant open file $ARGV[0]";

    while($line = <$file>){
        next if $. == 1;
        $line =~ m/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9] /;
        $start = $&;
        chomp($start);
        $start =~ s/^\s*(.*?)\s*$/$1/;

        @start_s = split(' ', $start);
        @start_t = split(':', $start_s[1]);
        $start_t[0] += 1;

        if($start_t[0] < 10){
            $start_t[0] = "0$start_t[0]";
        }

        $start1 = "$start_s[0] $start_t[0]:$start_t[1]";

        $line =~ m/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]/;
        $end = $&;
        chomp($end);

        $dateformat_start = "%F %R";
        $dateformat_end = "%F %T";

        chomp($dateformat_start);
        chomp($date_end);

        $date_start = Time::Piece->strptime($start1, $dateformat_start);
        $date_end = Time::Piece->strptime($end, $dateformat_end);

        if($date_end > $date_start){
            @line_s = split(';', $line);
            print "$line_s[0] $line_s[1] $line_s[2] - PROBLEM: $start --> $end\n"
        }
    }

    close $file;
}else{
   while($line = <>){
        next if $. == 1;
        $line =~ m/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9] /;
        $start = $&;
        chomp($start);
        $start =~ s/^\s*(.*?)\s*$/$1/;

        @start_s = split(' ', $start);
        @start_t = split(':', $start_s[1]);
        $start_t[0] += 1;

        if($start_t[0] < 10){
            $start_t[0] = "0$start_t[0]";
        }

        $start1 = "$start_s[0] $start_t[0]:$start_t[1]";

        $line =~ m/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]/;
        $end = $&;
        chomp($end);

        $dateformat_start = "%F %R";
        $dateformat_end = "%F %T";

        chomp($dateformat_start);
        chomp($date_end);

        $date_start = Time::Piece->strptime($start1, $dateformat_start);
        $date_end = Time::Piece->strptime($end, $dateformat_end);

        if($date_end > $date_start){
            @line_s = split(';', $line);
            print "$line_s[0] $line_s[1] $line_s[2] - PROBLEM: $start --> $end\n"
        }
    } 
}