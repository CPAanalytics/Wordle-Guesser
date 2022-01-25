from itertools import chain
from collections import Counter, OrderedDict
import numpy
from pprint import pprint
from english_words import english_words_lower_set


# attempts to guess wordle word in most efficient way possible.

def normalize_counter(counter):
    """Normalizes a Counter by dividing values by sum of values"""
    counter_total = float(sum(counter.values()))
    for key, value in counter.items():
        counter[key] /= counter_total
    return counter


def score_words(scoring_table, word):
    """Scores a word value by taking sum of char index probabilities and adding this to uniqueness score of overall
    char probabilities"""
    pos_value = 0
    for index, char in enumerate(word):
        probs = scoring_table[char]
        pos_value += probs[1][index]
    char_value = 0
    for char in set(word):
        char_value += scoring_table[char][0]
    return pos_value + char_value


def get_valid_wordle(english_words):
    """extracts valid wordle words from english dictionary"""
    valid_wordle = [i for i in english_words if len(i) == 5]
    return valid_wordle


def get_letter_dict(valid_wordle):
    """Creates counter of character occurences in wordle words"""
    letters = Counter(chain.from_iterable(valid_wordle))
    letters = normalize_counter(letters)
    return letters


def create_position_table(valid_wordle):
    """Creates table of index occurences by transposing list of word chars"""
    list_of_letters = [[i for i in chain.from_iterable(i)] for i in valid_wordle]
    np_list_of_letters = numpy.array(list_of_letters)
    transposed = np_list_of_letters.T
    transposed = transposed.tolist()
    return transposed


def get_scoring_table(letter_dict, position_table):
    """creates an index scoring table by combining normalized counters of position table with overall char score in
    tuple """
    new_dict = {}
    for key, value in letter_dict.items():
        new_dict[key] = (value, [])
        for index, letters in enumerate(position_table):
            counter = normalize_counter(Counter(letters))
            new_dict[key][1].append(counter[key])

    return new_dict


def get_scored_dict(scoring_table, valid_wordle):
    """creates dictionary of word scores"""
    scored_words = {}
    for words in valid_wordle:
        score = score_words(scoring_table, words)
        scored_words[words] = score
    return scored_words


def print_sorted_dict(dictionary):
    """Prints top 100 scoring words given a dictionary of word scores"""
    scored_keys = sorted(dictionary, key=scored_words.get)[-100:]
    scored_values = sorted(dictionary.values())[-100:]
    for item in zip(scored_keys, scored_values):
        print(item)


def filter_word_dict(scored_words, first_word, first_score):
    """filters a dictionary to possible values using word scores
    0 = black
    1 = yellow
    2 = green
    """
    new_dict = scored_words
    index = 0
    for char, score in zip(first_word, first_score):
        if score == 0:
            dict_cpy = {}
            for key, value in new_dict.items():
                if char in key:
                    continue
                else:
                    dict_cpy[key] = value
            new_dict = dict_cpy
        if score == 1:
            dict_cpy = {}
            for key, value in new_dict.items():
                if char in key and key[index] != char:
                    dict_cpy[key] = value
                else:
                    continue
            new_dict = dict_cpy
        if score == 2:
            dict_cpy = {}
            for key, value in new_dict.items():
                if key[index] == char:
                    dict_cpy[key] = value
                else:
                    continue
            new_dict = dict_cpy
        index += 1

    print_sorted_dict(new_dict)
    return new_dict


if __name__ == "__main__":
    valid_wordle = get_valid_wordle(english_words_lower_set)
    letter_dict = get_letter_dict(valid_wordle)
    position_table = create_position_table(valid_wordle)
    scoring_table = get_scoring_table(letter_dict, position_table)
    scored_words = get_scored_dict(scoring_table, valid_wordle)
    print_sorted_dict(scored_words)
    
    for i in range(1, 7):
        word = input("enter you word: ")
        parsed_word = [i for i in word]
        score = [int(i) for i in input("enter your score: ")]
        new_scored_words = filter_word_dict(scored_words, parsed_word, score)
        scored_words = new_scored_words
