#!/bin/bash

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

export SJAR=/usr/lib/hadoop/contrib/streaming/hadoop-streaming-0.20.2-CDH3B4.jar
export PROJECT=$1

echo "Deleting old data..."
hadoop fs -rmr $PROJECT

echo "Copying new data..."
hadoop fs -copyFromLocal $PROJECT $PROJECT

echo "Starting the job..."
# Please modify -numReduceTasks by hand for yoir data! This is fine for a 
# medium-sized workload, but choose something else for the full
# corpus.
hadoop jar $SJAR -mapper "word_tag_map.py" -reducer "dictionary_reduce.py" -input $PROJECT -output ${PROJECT}-out -numReduceTasks 233

echo "Copying the data back..."
hadoop fs -copyToLocal ${PROJECT}-out ${PROJECT}-out
