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
#    along with GraphingEnglish.  If not, see <http://www.gnu.org/licenses/>

import nltk
import fileinput
import re
from collections import defaultdict

# What a data line looks like:
# caterpillar/NN   She/PRP stretched/VBD herself/PRP up/RP on/IN tiptoe/NN ,/, and/CC peeped/VBD over/RP the/DT edge/NN of/IN the/DT mushroom/NN ,/, and/CC her/PRP$ eyes/NNS immediately/RB met/VBD those/DT of/IN a/DT large/JJ caterpillar/NN ,/, that/IN was/VBD sitting/VBG on/IN the/DT top/JJ with/IN its/PRP$ arms/NNS folded/VBD ,/, quietly/RB smoking/VBG a/DT long/JJ hookah/NN ,/, and/CC taking/VBG not/RB the/DT smallest/JJS notice/NN of/IN her/PRP$ or/CC of/IN anything/NN else/RB ./.

# DataLine class abstracts out the data format used in our reducer:
# a keyword, followed by a tab, then the sentence (with pos markers)
# that the word belongs to.
class DataLine:
	def __init__(self, line):
		self.line = line.strip()
		(word_pos, tab, example) = self.line.partition('\t')

		# The keyword parameter is the first word in the sentence
		self.keyword = breakWord(word_pos)
		
		# This is the rest of the sentence, also broken into words. Lets
		# look for the keyword here, while we are at it
		self.words = []
		self.position = -1

		example = cleanup_sentence(example)
		for word_pos in example.split(' '):
			this_word = breakWord(word_pos)
			self.words.append(this_word)

		for index, item in enumerate(self.words):
			if item == self.keyword:
				self.position = index
				break

	def beforeKey(self, delta):
		if self.position - delta < 0:
			return Word('', '')
		else:
			return self.words[self.position - delta]

	def afterKey(self, delta):
		if self.position + delta >= len(self.words):
			return Word('', '')
		else:
			return self.words[self.position + delta]
	
	def keyword(self):
		return self.keyword


def breakWord(word_pos):
	(word, slash, pos) = word_pos.partition('/')
	return Word(word, pos)

class Word:
	def __init__(self, word, pos):
		self.word = word.lower()
		self.pos = pos

	def __eq__(self, other):
		return self.word == other.word and self.pos == other.pos

	def __ne__(self, other):
		return not self.__eq__(other)

	def almost_equals(self, other):
		# Special case where we want to compare the text and the major part of
		# speech (N, V, etc), but not the secondary (NN, VP, etc)
		return self.word == other.word and self.pos[0] == other.pos[0]

	def pretty(self):
		return self.word + "/" + self.pos

	def word(self):
		return self.word

	def pos(self):
		return self.pos

	def isNoun(self):
		return re.match('^N', self.pos)

	def isAdjective(self):
		return re.match('^J', self.pos)

	def isVerb(self):
		return re.match('^V', self.pos)

	def isAdverb(self):
		# Hacky! The tagger is stupid, so let's filer on just 'ly'
		# words here...
		return re.match('^RB', self.pos) and re.search('ly$', self.word)

	def isToBe(self):
		tobe = ['be', 'am', 'is', 'are', 'were', 'was', 'being', 'been']
		return self.word in tobe

	def isToHave(self):
		tohave = [ 'have', 'has', 'had' ]
		return self.word in tohave

	def isConjunction(self):
		conjunctions = ['and', 'or']
		return self.word in conjunctions

	def isPreposition(self):
		preps = ['on', 'in', 'at', 'since', 'for', 'before', 'to', 'past', 'till', 'until', 'by', 'on', 'beside', 'under', 'below', 'over', 'above', 'across', 'through', 'into', 'towards', 'onto', 'from', 'off', 'about' ]
		return self.word in preps

	def isArticle(self):
		articles = ['a', 'an', 'the']
		return self.word in articles

class POSMap:
	def __init__(self, word_pos, related_pos):
		self.wordlist = {}
		self.wordmap = defaultdict(dict)
		self.wordname = word_pos
		self.relatedname = related_pos

	def clear(self):
		self.wordlist = {}
		self.wordmap = defaultdict(dict)

	def append_word(self, word):
		self.wordlist[word.word] = 'yes'

	def append_map(self, word, related_word):
		if related_word.word in self.wordmap[word.word]:
			self.wordmap[word.word][related_word.word] += 1
		else:
			self.wordmap[word.word][related_word.word] = 1

	def write_output(self):
		#print "We discovered " + str(len(self.wordlist)) + " " + self.wordname + "(s) and " + str(len(self.wordmap)) + " of them had " + self.relatedname + "(s)"

		keys = self.wordmap.keys()
		keys.sort()

		u_word_pos = self.wordname.upper()
		u_related_pos = self.relatedname.upper()

		for word in keys:

			print u_word_pos + "/" + u_related_pos + "\t" + word + ": ",
			akeys = self.wordmap[word].keys()
			akeys.sort(key=lambda  test: self.wordmap[word][test])
			akeys.reverse()
			for related_word in akeys:
				print related_word + "(" + str(self.wordmap[word][related_word]) + ") ",
			print

		
def cleanup_sentence(sent):
	# Remove punctuation
	temp = re.sub('[^A-Za-z\-\/\s]', '', sent)

	# leading and trailing dashes before the slash
	temp = re.sub('\-+/', '/', temp)
	temp = re.sub('\s+\-+', ' ', temp)

	# Remove words that were only punctuation...
	temp = re.sub('\s+\/\s+', ' ', temp)
	temp = re.sub('^/\s+', '', temp)
	temp = re.sub('\s+/$', '', temp)

	# Remove multiple spaces
	temp = re.sub('^\s+', '', temp)
	temp = re.sub('\s+$', '', temp)
	temp = re.sub('\s{2,}', ' ', temp)

	#print "temp: " + temp 
	return temp
		
def main():

	# Storage for our parts of speech lists
	nouns = POSMap('noun', 'adjective')
	verbs = POSMap('verb', 'adverb')
	adjectives = POSMap('adjective', 'noun')
	adverbs = POSMap('adverb', 'verb')

	# And more interesting examples
	direct_objects = POSMap('verb', 'direct object')
	
	lastword = Word('', '')

	for line_data in fileinput.input():
		line = DataLine(line_data)

		word = line.keyword

		# Is this a new word? First, dump out all the previous key's data
		#print "Comparing " + word.word() + " to " + "lastword.word()"
		if not word.almost_equals(lastword):
			#print "Didn't match '" + word.pretty() + "' to '" + lastword.pretty() + "'"
			if lastword.isNoun():
				nouns.write_output()
				nouns.clear()
			elif lastword.isVerb():
				verbs.write_output()
				direct_objects.write_output()
				verbs.clear()
				direct_objects.clear()
			elif lastword.isAdjective():
				adjectives.write_output()
				adjectives.clear()
			elif lastword.isAdverb():
				adverbs.write_output()
				adverbs.clear()
			
			lastword = word

			
		if (word.isNoun()):
			# We have a noun, add to the list
			nouns.append_word(word)

			# Now, we want to find the common adjectives for this noun
			preword = line.beforeKey(1)
			if preword.isAdjective():
				nouns.append_map(word, preword)

				# Now, look for more adjectives before this one in a chain
				relative_position = 2
				test = line.beforeKey(relative_position)
				while test.isAdjective() or test.isConjunction():
					relative_position += 1
					if test.isAdjective():
						nouns.append_map(word, test)
					test = line.beforeKey(relative_position)

		if word.isVerb():
			# We have a verb, add to the list
			verbs.append_word(word)

			# We need the common adverbs for this verb, which can be found
			# either before or after the verb
			for poss in [ line.beforeKey(1), line.afterKey(1) ]:
				if poss.isAdverb():
					verbs.append_map(word, poss)

			# Todo, add chain detection later. 

			# Let's also check for direct objects
			if line.afterKey(1).isPreposition():
				place = 2
				while line.afterKey(place).isArticle() or line.afterKey(place).isNoun() or line.afterKey(place).isAdjective():
					if line.afterKey(place).isNoun():
						direct_objects.append_map(word, line.afterKey(place))
						break
					place += 1
				

		if word.isAdjective():
			# We have an adjective, look for related nouns
			adjectives.append_word(word)
			postword = line.afterKey(1)
			if (postword.isNoun()):
				adjectives.append_map(word, postword)

		if word.isAdverb():
			adverbs.append_word(word)
			for poss in [ line.beforeKey(1), line.afterKey(1) ]:
				if poss.isVerb():
					# Now, we don't want forms of 'to have' or 'to be' here
					# because this will catch them incorrectly
					if poss.isToHave() or poss.isToBe():
						continue
					adverbs.append_map(word, poss)
			

	# We're at the end, dump out whatever is left...
	nouns.write_output()
	verbs.write_output()
	adjectives.write_output()
	adverbs.write_output()
	direct_objects.write_output()

# Run the program
if __name__ == "__main__":
	main()

