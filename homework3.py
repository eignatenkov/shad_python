from collections import Counter
import os
import json
from nltk.tokenize import RegexpTokenizer

root_dir = 'corpus'

single_stats = dict()
double_stats = dict()

tokenizer = RegexpTokenizer('\w+(\')?\w+(\.)?')

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        with open(os.path.join(subdir, file)) as f:
            for line in f:
                clean_line = line.decode('unicode_escape').encode('ascii','ignore').lower()
                clean_line = clean_line.replace('-', ' ')
                words = tokenizer.tokenize(clean_line)
                for index, word in enumerate(words):
                    true_word = word.strip('.')
                    if not true_word:
                        continue
                    if true_word not in single_stats:
                            single_stats[word.strip('.')] = Counter()
                    if word[-1] == '.':
                            single_stats[true_word]['.'] += 1
                    elif index < len(words) - 1:
                        single_stats[true_word][words[index+1].strip('.')] += 1
                        double_key = true_word + ' ' + words[index+1].strip('.')
                        if double_key not in double_stats:
                            double_stats[double_key] = Counter()
                        if index == len(words) - 2:
                            double_stats[double_key]['.'] += 1
                        else:
                            if words[index+1][-1] == '.':
                                double_stats[double_key]['.'] += 1
                            else:
                                double_stats[double_key][words[index+2].strip('.')] += 1
        print 'done with ', file

# single_stats = dict((k, v) for k, v in single_stats.iteritems() if v)
# double_stats = dict((k, v) for k, v in double_stats.iteritems() if v)

with open("single_stats.txt", "w") as fw:
    json.dump(single_stats, fw)
with open("double_stats.txt", "w") as fw:
    json.dump(double_stats, fw)
