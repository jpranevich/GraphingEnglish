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

# This script acts as a "map" in a map/reduce pair, generating output of
# keyword <tab> example. We need to leave as much context in the example as we
# can, but we don't need to include the full sentence.

import nltk
import fileinput
import re

def context(num_words, word, text_tagged):
	# Print out num_words of context around the word in the tagged list.
	# But, if our word appears more than once, we should return the whole text.
	# (FIXME - there may be a better way to do this)

	# First, find out where we are...
	#print "Looking for " + str(word) + " in " + str(text_tagged)

	i = text_tagged.index(word)
	start = max(0, i - num_words)
	end = min(len(text_tagged), i + num_words + 1)
	return text_tagged[start:end]
	
def inline_write_tags (text_tagged):
	# We get a list of tagged tuples and managed them baxk into 
	# a string
	out = ""
	for word in text_tagged:
		out += " " + word[0] + "/" + word[1]
	
	return out

def cleanup_word(word_pos):
	# Downcase the word and remove the punctuation
	word = re.sub('^[\'\"\-_]+', '', word_pos[0])
	word = re.sub('[\'\"\-_\.\!\?\,\;]*$', '', word)
	word = word.lower()
	return (word, word_pos[1])
	
def just_letters(word_pos):
	return re.search('^[A-Za-z\-\']+$', word_pos[0])
	
def wanted_pos(word_pos):
	# We want nouns (N), verbs (V), adjectives, and adverbs, and no proper
	# nouns (NNP)
	return (re.match('^[JNVR]', word_pos[1])) and (word_pos[1] != 'NNP')
	

def main():
	for sent in fileinput.input():
		sent = sent.rstrip()

		# Word tokenizer can't deal with -- as punctuation, replace
		# (not optimally) with ,
		sent = re.sub('--', ', ', sent)

		text = nltk.word_tokenize(sent)
		text_tagged = nltk.pos_tag(text)

		# Cleanup the list, remove punct and lowercase it
		text_tagged = map(cleanup_word, text_tagged)

		# Now, run the filters for words and correct parts of speech
		text_tagged = filter(just_letters, text_tagged)
		words_to_report = filter(wanted_pos, text_tagged)

		for word in words_to_report:
			print word[0] + "/" + word[1] + "\t" + inline_write_tags(context(4, word, text_tagged))

		
# Run the program
if __name__ == "__main__":
    main()

		
