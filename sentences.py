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

import nltk
import re
import fileinput
import sys

for this_file in sys.argv[1:]:
	f = open(this_file, 'r')

	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

	# First, we do want to consider as separate sentences units that are \n\s*\n
	two_blanks = re.compile('(\s*\n\s*){2,}')
	rem_spaces = re.compile('\s+')
	any_text = re.compile('[A-Za-z]')

	# We need to ignore all text before "START OF THIS PROJECT GUTENBERG EBOOK"
	whole_file = f.read().strip()

	# START OF THE PROJECT GUTENBERG
	find_start = re.compile('^.*?START OF (THIS|THE) PROJECT GUTENBERG.*?\n+', re.S)

	# Annoying inconsistent end-of-text markers.

	# End of Project Gutenberg's The Three Musketeers, by Alexandre Dumas, Pere
	# *** END OF THIS PROJECT GUTENBERG EBOOK THE THREE MUSKETEERS ***
	# ***END OF THE PROJECT GUTENBERG EBOOK HEBRAIC

	find_end = re.compile('\nEnd of( the)? Project Gutenberg.*?$', re.S)
	find_end2 = re.compile('\n\s*\*+\s*END OF (THIS|THE) PROJECT GUTENBERG.*?$', re.S)

	whole_file = find_end.sub('', find_start.sub('', whole_file))
	whole_file = find_end2.sub('', whole_file)

	for paragraph in two_blanks.split(whole_file):
		sents = sent_detector.tokenize(paragraph, realign_boundaries=True)

		for sent in sents:
			sent = rem_spaces.sub(' ', sent)
			if any_text.search(sent):
				print sent
