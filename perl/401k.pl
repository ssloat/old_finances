use strict;
use warnings;

use File::Slurp 'read_file';
use Data::Dumper;

chomp(my @lines = read_file('files/401k 2014.htm'));

my $table = q{};
my $rec=0;
for my $l (@lines) {
    if ($l =~ m#.*<table ([^/]*?)>#) {
        my $table = $1;
        my %kvs = map {split /=/} grep {s/"//g} split /\s+/, $table;
        if (($kvs{'id'} // q{}) eq 'sortable') {
            $rec=1;
        }
    }
    elsif ($l =~ m#.*</table>.*#) {
        $rec=0;
    }
    elsif ($rec) {
        ($l) = ($l =~ m#\s*(.*)\s*#);
        $table .= " $l";
    }
}

my @entries;
for my $row ($table =~ m#(<tr[ >].*?</tr>)#g) {
    my @tds = ($row =~ m#<td.*?>\s*(.*?)\s*?</td>#g);
    s/<.*?>//g for @tds;
    next if !@tds;
    if ($tds[0] =~ m#^(\d\d/\d\d/\d\d\d\d)#) {
        push @entries, [$1, @tds[1, 2]];
    }
    elsif ($tds[1] ne 'Sources') {
        push @{ $entries[-1] }, [@tds[1..$#tds]];
    }
}


my %types;
for (@entries) {
    my @entry = @$_;
    next if $entry[2] ne 'CONTRIBUTION';

    for my $item (@entry[3..$#entry]) {
        next if !$item->[0];
        my $k = $item->[0] eq '07 - PRE TAX CONTRIBUTIONS' ? 'me' : 'BofA';

        my $amt = substr $item->[1], 1;
        $amt =~ s/,//g;
        print "$entry[0], $entry[1], $k, $amt\n";
        $types{$k} += $amt;
    }
}

print Dumper(\%types) . "\n";
