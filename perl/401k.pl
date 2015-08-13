use strict;
use warnings;

use File::Slurp 'read_file';
use Data::Dumper;
use Carp;

#chomp(my @lines = read_file('../files/401k 2014.htm'));
chomp(my @lines = read_file($ARGV[0]));

my $table = q{};
for my $line (@lines) {
    if ($line =~ m#.*<table ([^/]*?)>#) {
        my $match = $1;
        if ($match =~ m#id="sortable"#) {
            $table = $match;
            #my %kvs = map {split /=/} grep {s/"//g} split /\s+/, $match;
            #if (($kvs{'id'} // q{}) eq 'sortable') {
            #    $table = $match;
            #}
        }
    }
    elsif ($table) {
        last if $line =~ m#.*</table>.*#;
        my ($l) = ($line =~ m#\s*(.*)\s*#);
        $table .= " $l";
    }
}

my @entries;
for my $row ($table =~ m#(<tr[ >].*?</tr>)#g) {
    my @tds = ($row =~ m#<td.*?>\s*(.*?)\s*?</td>#g);
    s/<.*?>//g for @tds;
    next if !@tds;
    if ($tds[0] =~ m#^(\d\d/\d\d/\d\d\d\d)#) {
        push @entries, [$1, @tds[1..4]];
    }
    elsif ($tds[1] ne 'Sources') {
        push @{ $entries[-1] }, [@tds[1..$#tds]];
    }
}


my %types;
for (@entries) {
    my @entry = @$_;
    if ($entry[2] eq 'CONTRIBUTION' || $entry[2] eq 'Transfer In/Out' || $entry[2] eq 'Investment Gain (Loss)') {
        $entry[4] =~ s/,//g;
        next if $entry[4] == 0;

        for my $item (@entry[5..$#entry]) {
            next if !$item->[0];
            my $k = 
                $item->[0] eq '07 - PRE TAX CONTRIBUTIONS'  ? 'Personal Contrib' 
              : $item->[0] eq '14 - SAFE HARBOR MATCH'      ? 'BofA Match' 
              : $item->[0] eq '17 - PRE SAFE HARBOR MATCH'  ? 'BofA Match' 
              : $item->[0] eq '01 - MATCH I'                ? 'BofA Match' 
              : $item->[0] eq '04 - MATCH V/STOCK FUND DIV' ? 'BofA Match' 
              : $item->[0] eq '20 - ANNUAL COMPANY CONTRIB' ? 'Pension' 
              : $item->[0] eq '16 - REWARDING SUCCESS PLAN' ? 'Rewarding Success' 
              : $item->[0] eq '01 - POST 2007 COMP CREDITS' ? 'Pension Credit' 
              : $item->[0] eq '05 - PRE-2008 COMP CREDITS'  ? 'Pension Credit' 
              : $item->[0] eq '13 - QNEC'                   ? 'QNEC' 
              : confess "Unknown Contribution:  $item->[0]";

            $item->[1] =~ s/[\$,]//g;
            print "$entry[0],$entry[1],$k,$item->[1],$item->[2]\n";
            $types{$k} += $item->[1];
        }
    }
    elsif ($entry[2] eq 'Dividends' || $entry[2] eq 'RECORDKEEPING FEE'
        || $entry[2] eq 'Exchanges' || $entry[2] eq 'Adjustments'
        || $entry[2] eq 'TRUSTEE FEE'
    ) {
        $entry[3] =~ s/[\$,]//g;
        $entry[4] =~ s/[\$,]//g;
        print "$entry[0],$entry[1],$entry[2],$entry[3],$entry[4]\n";
        $types{$entry[2]} += $entry[3];
    }
    #elsif ($entry[2] eq 'Investment Gain (Loss)' || $entry[2] eq 'Transfer In/Out') {
    elsif ($entry[2] eq 'Investment Gain (Loss)') {
        next if $entry[4] == 0;
        print "$entry[0],$entry[1],$entry[2],$entry[3],$entry[4]\n";
    }
    else {
        confess "Unknown Action --$entry[2]: @entry\n";
    }
}

#print Dumper(\%types) . "\n";
