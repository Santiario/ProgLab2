__author__ = 'Vemund'
# -*- coding=utf-8 -*-
from os import listdir
from os.path import isfile, join
import operator
import math


class FileHandler:

    @staticmethod
    def read_file(filepath):
        file = open(filepath, 'r')
        string = ''
        for line in file.readlines():
            string += line.strip() + ' '
        return string.lower()

    @staticmethod
    def make_filepath_list(directory):
        return [directory + f for f in listdir(directory) if isfile(join(directory, f))]


class StringHandler:

    @staticmethod
    def remove_nonalphanumeric(string):
        result = ''
        string = string.replace('<br />', '')
        for char in string:
            if char.isalnum() or char == ' ':
                result += char
        return result

    @staticmethod
    def make_set_from_string(string):
        return set(string.split())



    def make_word_scores(self, pos_filepaths, neg_filepaths, stop_words):
        pos_ordbok = self.make_dict(pos_filepaths)
        neg_ordbok = self.make_dict(neg_filepaths)
        self.remove_stop_words(pos_ordbok, stop_words)
        self.remove_stop_words(neg_ordbok, stop_words)
        # Pruning
        self.prune(pos_ordbok, len(pos_filepaths) + len(neg_filepaths), 10)
        self.prune(neg_ordbok, len(pos_filepaths) + len(neg_filepaths), 10)

        for key in pos_ordbok.keys():
            if neg_ordbok.get(key) is None:

                pos_ordbok[key] /= float(pos_ordbok[key])
            else:
                pos_ordbok[key] /= float(pos_ordbok[key] + neg_ordbok[key])

        for key in neg_ordbok.keys():
            if pos_ordbok.get(key) is None:
                neg_ordbok[key] /= float(neg_ordbok[key])
            else:
                neg_ordbok[key] /= float(pos_ordbok[key] + neg_ordbok[key])

        return sorted(pos_ordbok.items(), key=operator.itemgetter(1), reverse=True), sorted(neg_ordbok.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def remove_stop_words(dictionary, stop_words):
        for word in stop_words:
            dictionary.pop(word, None)

    def make_dict(self, filepaths):
        ordbok = {}
        for filepath in filepaths:
            word_set = self.make_set_from_string(self.remove_nonalphanumeric(FileHandler.read_file(filepath)))
            for word in word_set:
                """if word == 'onstreet':
                    print(filepath, 'Fant onstreet!')"""
                    # Used to find typos and other misspelled words during implementing
                if ordbok.get(word) is None:
                    ordbok[word] = 1
                else:
                    ordbok[word] += 1
        return ordbok

    def prune(self, dictionary, number_of_texts, percentage):
        sett = set(dictionary.keys())
        for key in sett:
            if dictionary[key] < int(math.floor((percentage * number_of_texts)/100.0)):
                dictionary.pop(key, None)

class CollectionHandler:
    pass

if __name__ == '__main__':
    f = FileHandler()
    s = StringHandler()
    stop_words = s.make_set_from_string(s.remove_nonalphanumeric(f.read_file('./data/stop_words.txt')))
    positive_filepaths = f.make_filepath_list('./data/subset/train/pos/')
    negative_filepaths = f.make_filepath_list('./data/subset/train/neg/')
    positive_scores, negative_scores = s.make_word_scores(positive_filepaths,negative_filepaths, stop_words)
    print('positive:', positive_scores)
    print('negative:', negative_scores)
