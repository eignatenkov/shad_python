import json
import random


def weighted_choice(choices):
    total = sum(choices.values())
    r = random.uniform(0, total)
    upto = 0
    for key in choices:
        if upto + choices[key] >= r:
            return key
        upto += choices[key]

with open("single_stats.txt") as f:
    single_stats = json.load(f)
with open("double_stats.txt") as f:
    double_stats = json.load(f)

prev = '.'
line = ''
for i in range(10000):
    if prev[-1] == '.':
        next_word = weighted_choice(single_stats["start sentence"]).title()
        prev = next_word.lower()
    elif len(prev.split(' ')) == 1:
        next_word = weighted_choice(single_stats[prev])
        prev = prev+' '+next_word
    else:
        next_word = weighted_choice(double_stats[prev])
        prev = prev.split(' ')[-1] + ' ' + next_word
    if next_word == '.':
        line += '.'
    else:
        line += ' ' + next_word

print line
