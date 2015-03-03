use strict;
use warnings;

use File::Slurp 'read_file';
use Data::Dumper;

chomp(my @lines = read_file('files/401k 2014.htm'));

my $table = q{};
for my $line (@lines) {
    if ($line =~ m#.*<table ([^/]*?)>#) {
        my %kvs = map {split /=/} grep {s/"//g} split /\s+/, $1;
        if (($kvs{'id'} // q{}) eq 'sortable') {
            $table = $1;
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
    if ($entry[2] eq 'CONTRIBUTION') {

        for my $item (@entry[5..$#entry]) {
            next if !$item->[0];
            my $k = 
                $item->[0] eq '07 - PRE TAX CONTRIBUTIONS'  ? 'me' 
              : $item->[0] eq '14 - SAFE HARBOR MATCH'      ? 'BofA Match' 
              : $item->[0] eq '20 - ANNUAL COMPANY CONTRIB' ? 'Pension' 
              : undef;

            if (!$k) {
                print "Unknown:  $item->[0]\n";
                next;
            }

            $item->[1] =~ s/[\$,]//g;
            print "$entry[0], $entry[1], $k, $item->[1], $item->[2]\n";
            $types{$k} += $item->[1];
        }
    }
    elsif ($entry[2] eq 'Dividends' || $entry[2] eq 'RECORDKEEPING FEE') {
        $entry[3] =~ s/[\$,]//g;
        print "$entry[0], $entry[1], $entry[2], $entry[3], $entry[4]\n";
        $types{$entry[2]} += $entry[3];
    }
}

print Dumper(\%types) . "\n";
