# -*- coding: utf-8 -*-
import json
import random


def weighted_choice(choices):
    """
    функция случайного выбора из распределения частот
    :param choices: словарь с натуральными значениями, которые трактуются как
    частота ключей
    :return: ключ из choices, выбранный случайным образом с учетом частот ключей
    """
    total = sum(choices.values())
    r = random.uniform(0, total)
    upto = 0
    for key in choices:
        if upto + choices[key] >= r:
            return key
        upto += choices[key]


def text_generation(length, path_to_stats=''):
    """
    Генерация случайного текста с помощью цепей Маркова
    :param length: длина текста
    :param path_to_stats: путь к файлам со статистиками
    :return: сгенерированный текст
    """

    with open(path_to_stats+"single_stats.txt") as f:
        single_stats = json.load(f)
    with open(path_to_stats+"double_stats.txt") as f:
        double_stats = json.load(f)

    prev = '.'
    text = ''
    for i in range(length):
        # если перед словом была точка, выбираем случайное слово из тех, которые
        # были началом предложения
        if prev[-1] == '.':
            next_word = weighted_choice(single_stats["start sentence"]).title()
            prev = next_word.lower()
        # если предыдущая цепь из одного слова, берем следующее из single-
        # распределения
        elif len(prev.split(' ')) == 1:
            next_word = weighted_choice(single_stats[prev])
            prev = prev+' '+next_word
        # в обычной ситуации берем слово из double-распределения
        else:
            next_word = weighted_choice(double_stats[prev])
            prev = prev.split(' ')[-1] + ' ' + next_word
        # Обработка прихода в точку.
        if next_word == '.':
            text += '.'
        else:
            text += ' ' + next_word

    return text
    
if __name__ == "__main__":
    with open ("random_text.txt", "w") as f:
        f.write(text_generation(10000))

