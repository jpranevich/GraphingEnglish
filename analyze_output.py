#!/usr/bin/python

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

# Quick script to write some output about a word

datafile = "datafile-half-gutenberg.txt"

import sys
import re

def main():
	target_pos = sys.argv[1]
	target = sys.argv[2]


	if target_pos == 'noun':
		target_tag = 'NOUN/ADJECTIVE'
		target_desc = ('noun', 'adjective(s)')
	elif target_pos == 'adjective':
		target_desc = ('adjective', 'noun(s)')
		target_tag = 'ADJECTIVE/NOUN'
	elif target_pos == 'verb':
		target_tag = 'VERB/ADVERB'
		target_desc = ('verb', 'adverb(s)')
	elif target_pos == 'adverb':
		target_tag = 'ADVERB/VERB'
		target_desc = ('adverb', 'verb(s)')
	elif target_pos == 'object':
		target_tag = 'VERB/DIRECT OBJECT'
		target_desc = ('verb', 'direct object(s)')
	else:
		target_tag = 'UNKNOWN'
		target_desc = ('unknown', 'unknown')

	f = open(datafile, 'r')
	for line in f.readlines():
		(header, data) = line.split("\t")
		(word, values) = data.split(":")

		if word == target and header == target_tag:
			display_output(header, word, values, target_desc)


def display_output(header, word, values, target_desc):
	# First, process the values
	value_list = values.split()
	value_list = map(parse_word_num, value_list)
	occurances = sum_up(value_list)

	how_many = len(value_list)
	print "We have " + str(how_many) + " " + target_desc[1] + " found for this " + target_desc[0] + " (In " + str(occurances) + " appearances in the corpus.)"

	for word_pair in value_list[:20]:
		graph_it(word_pair[0], int(word_pair[1]), occurances)

	
def graph_it(word, numerator, denominator):
	print word + " " + str(int(numerator * 100/denominator)) + "%\t" + ("#" * int(numerator * 60 /denominator))

def sum_up(value_list):
	# Get the sum of all values in the list
	mysum = 0
	for item in value_list:
		mysum += int(item[1])
	return mysum

def parse_word_num(word_num):
	(word, num) = re.match('(.+)\((\d+)\)', word_num).groups()
	return (word, num)

# Run the program
if __name__ == "__main__":
    main()

