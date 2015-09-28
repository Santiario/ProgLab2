__author__ = 'Vemund'
# -*- coding=utf-8 -*-
from os import listdir
from os.path import isfile, join
import operator


class FileHandler:

    def read_file(self, filepath):
        file = open(filepath, 'r')
        string = ''
        for line in file.readlines():
            string += line.strip() + ' '
        return string.lower()

    def remove_nonalphanumeric(self, string):
        result = ''
        for char in string:
            if char.isalnum() or char == ' ':
                result += char
        return result

    def make_set(self, string):
        return set(string.split())

    def make_filepath_list(self, directory):
        return [directory + f for f in listdir(directory) if isfile(join(directory, f))]

    def remove_words(self, set1, set2):
        return set1 - set2

    def make_word_score(self, filepaths, stop_words):
        ordbok = {}

        for filepath in filepaths:
            word_set = self.remove_words(self.make_set(self.remove_nonalphanumeric(self.read_file(filepath))), stop_words)
            for word in word_set:
                if ordbok.get(word) is None:
                    ordbok[word] = 1
                else:
                    ordbok[word] += 1
        for word in ordbok:
            ordbok[word] /= float(len(filepaths))
        return sorted(ordbok.items(), key=operator.itemgetter(1), reverse=True)


class CollectionGenerator:
    pass

if __name__ == '__main__':
    f = FileHandler()
    stop_words = f.make_set(f.remove_nonalphanumeric(f.read_file('./data/stop_words.txt')))
    positive_filepaths = f.make_filepath_list('./data/subset/train/pos/')
    positive_ordbok_popularity_tuples = f.make_word_score(positive_filepaths, stop_words)
    print(positive_ordbok_popularity_tuples)
    negative_filepaths = f.make_filepath_list('./data/subset/train/neg/')
    negative_ordbok_popularity_tuples = f.make_word_score(negative_filepaths, stop_words)
    print(negative_ordbok_popularity_tuples)

