__author__ = 'Vemund'
# -*- coding=utf-8 -*-
from os import listdir
from os.path import isfile, join
import operator


class FileHandler:

    @staticmethod
    def read_file(filepath):
        file = open(filepath, 'r')
        string = ''
        for line in file.readlines():
            string += line.strip() + ' '
        """if (filepath[:23] == './data/subset/train/pos'):
            if  ('hidden' in string):
                #print('Hidden found in a negative string!')
                FileHandler.pos_hidden += 1
        if (filepath[:23] == './data/subset/train/neg'):
            if  ('hidden' in string):
                #print('Hidden found in a negative string!')
                FileHandler.neg_hidden += 1"""
        return string.lower()

    @staticmethod
    def make_filepath_list(directory):
        return [directory + f for f in listdir(directory) if isfile(join(directory, f))]

    def make_list_from_file(self, filepath):
        return ' '.join(open(filepath).readlines()).split()


class Word:
    def __init__(self, string):
        self.string = string
        self.appeared = 1
        self.popularity = 0
        self.information_value = 0

    def __str__(self):
        return self.string

    def __unicode__(self):
        return self.string

    def __repr__(self):
        return self.string + '. Appeared: ' + str(self.appeared) + '. Popularity:' + str(self.popularity) + \
               '. InfoValue: ' + str(self.information_value) + '\n'

    def __eq__(self, other):
        if self.string == other.string:
            return True
        return False

    def __add__(self, other):
        self.string += ' ' + other.string
        return self

    def __lt__(self, other):
        return self.information_value < other.information_value

    def calculate_popularity(self, number_of_files):
        self.popularity = self.appeared/number_of_files


class Dictionary:

    def __init__(self):
        self.words = dict()

    def __repr__(self):
        return self.words

    def values(self):
        return self.words.values()

    def keys(self):
        return self.words.keys()

    def items(self):
        return self.words.items()

    def get_appeared(self, word):
        if word in self.words.keys():
            return self.words[word].appeared
        else:
            return 0

    @staticmethod
    def remove_nonalphanumeric(string):
        result = ''
        string = string.replace('<br />', ' ')
        for char in string:
            if char.isalnum() or char == ' ':
                result += char
        return result

    def remove_word(self, word):
        self.words.pop(word, None)

    def remove_words(self, word_list):
        for word in word_list:
            self.remove_word(word)



    def make_word_scores(self, pos_filepaths, neg_filepaths, stop_words, percentage, n_gram):

        # Pruning
        self.prune(pos_ordbok, neg_ordbok, len(pos_filepaths) + len(neg_filepaths), percentage)


    def make_words_from_filepaths(self, filepaths):
        for filepath in filepaths:
            string_set = set(self.remove_nonalphanumeric(FileHandler.read_file(filepath)).split())
            for string in string_set:
                #if string == 'portraywhiteonblackviolenceandwinanoscar':
                #    print(filepath, string)
                if string in self.words.keys():
                    self.words[string].appeared += 1
                else:
                    self.words[string] = Word(string)



    def make_dict(self, filepaths, n_gram=1):
        ordbok = {}
        for filepath in filepaths:
            word_list = self.remove_nonalphanumeric(FileHandler.read_file(filepath)).split()
            word_set = set()
            for i in range(1, n_gram + 1):
                index = 0
                while index < len(word_list) - i:
                    word = ''
                    for j in range(i):
                        word += word_list[index + j] + ' '
                    word = word[:-1]
                    if word not in word_set:
                        pass
                        # print('La til:', word, 'i ordlista.')
                    word_set.add(word)
                    index += 1
                for word in word_set:
                    if word == 'pornnow':
                        print(filepath, 'Fant pornnow!')
                    # Used to find typos and other misspelled words during implementing
                    if ordbok.get(word) is None:
                        ordbok[word] = 1
                    else:
                        ordbok[word] += 1
        return ordbok

    def prune(self, pos_ordbok, neg_ordbok, number_of_texts, percentage):
        keys = set(pos_ordbok.keys()).union(neg_ordbok.keys())
        for key in keys:
            total = 0
            if neg_ordbok.get(key) is not None:
                total += neg_ordbok[key]
            if pos_ordbok.get(key) is not None:
                total += pos_ordbok[key]

            if neg_ordbok.get(key) is not None:
                neg_ordbok[key] /= total
            if pos_ordbok.get(key) is not None:
                pos_ordbok[key] /= total

        for key in neg_ordbok.keys():
            if pos_ordbok.get(key) is None:
                neg_ordbok[key] /= float(neg_ordbok[key])
            else:
                neg_ordbok[key] /= float(pos_ordbok[key] + neg_ordbok[key])
        for key in keys:
            if key == 'hidden':
                print(number_of_texts)
            if dictionary[key]/number_of_texts <= percentage/100.0:
                dictionary.pop(key, None)
            """else:
                print(dictionary[key]/number_of_texts)"""


if __name__ == '__main__':
    f = FileHandler()
    positive_words = Dictionary()
    negative_words = Dictionary()
    stop_words = f.make_list_from_file('./data/stop_words.txt')

    positive_filepaths = f.make_filepath_list('./data/subset/train/pos/')
    negative_filepaths = f.make_filepath_list('./data/subset/train/neg/')

    positive_words.make_words_from_filepaths(positive_filepaths)
    negative_words.make_words_from_filepaths(negative_filepaths)

    for word in positive_words.values():
        word.calculate_popularity(len(positive_filepaths))
    for word in negative_words.values():
        word.calculate_popularity(len(negative_filepaths))

    positive_words.remove_words(stop_words)
    negative_words.remove_words(stop_words)

    for word in positive_words.values():
        total_appeared = positive_words.get_appeared(word.string) + negative_words.get_appeared(word.string)
        word.information_value = word.appeared / total_appeared
    for word in negative_words.values():
        total_appeared = positive_words.get_appeared(word.string) + negative_words.get_appeared(word.string)
        word.information_value = word.appeared / total_appeared

    print(sorted(positive_words.items(), key=operator.itemgetter(1)))
    print(sorted(negative_words.items(), key=operator.itemgetter(1)))


    #positive_scores, negative_scores = s.make_word_scores(positive_filepaths, negative_filepaths, stop_words, 1, n_gram=2)
    #print(FileHandler.num /(len(positive_filepaths) + len(negative_filepaths)))
    #print(len(negative_filepaths))
    #print(len(negative_filepaths))
    #print('positive:', positive_scores)
    #print('negative:', negative_scores)
