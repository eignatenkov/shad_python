from collections import Counter
import os
import json
from nltk.tokenize import RegexpTokenizer

def generate_statistics(root_dir):

    single_stats = dict() 
    double_stats = dict()
    
    single_stats["start sentence"] = Counter()
    
    tokenizer = RegexpTokenizer('\w+[\']?\w+[\.]?')

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
                        if index == 0:
                            single_stats["start sentence"][true_word] += 1
                        if true_word not in single_stats:
                                single_stats[word.strip('.')] = Counter()
                        if word[-1] == '.':
                                single_stats[true_word]['.'] += 1
                                if index < len(words) - 1:
                                    single_stats["start sentence"][words[index+1].strip('.')] += 1
                                
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
                        else:
                            single_stats[true_word]['.'] += 1
                            
            print 'done with ', file

    with open("single_stats.txt", "w") as single_stats_file:
        json.dump(single_stats, single_stats_file)
    with open("double_stats.txt", "w") as double_stats_file:
        json.dump(double_stats, double_stats_file)

if __name__ == "__main__":
    root_dir = '/home/egor/Dropbox/yandexdataschool/python/Homework 3/corpus'
    generate_statistics(root_dir)
