#!/usr/bin/perl -w

# Copyright 2011, Joe Pranevich

# This file is part of GraphingEnglish.
#
#    GraphingEnglish is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GraphingEnglish is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GraphingEnglish.  If not, see <http://www.gnu.org/licenses/>.

use strict;

# Quick wrapper to sort on tabs, since unix sort sucks
sub main {

	my %keys;
	my %values;
	while (my $line = <>) {
		my ($key, $value) = ($line =~ m/^(.*?)\t(.*)$/);
		$keys{$key} = 1;
		unless (defined($values{$key})) {
			@{$values{$key}} = ($value);
		} else {
			push(@{$values{$key}}, $value);
		}
	}

	my @skeys = sort(keys %keys);
	foreach my $key (@skeys) {
		foreach my $value (@{$values{$key}}) {
			print "$key\t$value\n";
		}
	}
}

main;
