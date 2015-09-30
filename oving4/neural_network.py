__author__ = 'Vemund'
# -*- coding=utf-8 -*-
from os import listdir
from os.path import isfile, join
import math as m


class FileHandler:

    @staticmethod
    def read_file(filepath):
        file = open(filepath, 'r', encoding="utf8")
        string = ''
        for line in file.readlines():
            string += line.strip() + ' '
        return string.lower()

    @staticmethod
    def make_filepath_list(directory):
        return [directory + f for f in listdir(directory) if isfile(join(directory, f))]

    @staticmethod
    def make_list_from_file(filepath):
        return ' '.join(open(filepath, 'r', encoding='utf8').readlines()).split()


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
        return self.string.rjust(15) + str('  Appeared: ' + str(self.appeared)).ljust(20) + str('  Popularity:' +
                str(self.popularity)).ljust(30) + str('  InfoValue: ' + str(self.information_value)).ljust(15)

    def __eq__(self, other):
        if self.string == other.string:
            return True
        return False

    def __add__(self, other):
        self.string += ' ' + other.string
        return self

    def __lt__(self, other):
        return self.popularity < other.popularity

    def calculate_popularity(self, number_of_files):
        #print('Word', self.string, 'appeared', self.appeared, 'times. Popularity:', self.appeared/number_of_files)
        self.popularity = self.appeared/number_of_files


class Dictionary:

    def __init__(self, name):
        self.name = name
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

    def get_popularity(self, word):
        if word in self.words.keys():
            return self.words[word].popularity
        else:
            return 0

    def get_word(self, string):
        return self.words.get(string)

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

    def get_words_as_strings(self):
        strings = []
        for word in self.words.values():
            strings.append(word.string)
        return strings

    def remove_words(self, word_list):
        for word in word_list:
            self.remove_word(word)

    def set_info_value(self, word, total_appeared):
        if self.words.get(word) is None:
            pass
        else:
            self.words[word].information_value = self.words[word].appeared / total_appeared

    def make_words_from_filepaths(self, filepaths, n_grams=1):
        for filepath in filepaths:
            word_list = self.remove_nonalphanumeric(FileHandler.read_file(filepath)).split()
            #print(word_list)
            for n in range(1, n_grams + 1):
                word_set = set()
                index = 0
                while index <= len(word_list) - n:
                    word = ' '.join(word_list[index:index + n])
                    if word not in word_set:
                        if word == 'downloading' and self.name == 'negative':
                            print('Found downloading')
                        word_set.add(word)
                        if word in self.words.keys():
                            self.words[word].appeared += 1
                        else:
                            self.words[word] = Word(word)
                    index += 1

    def prune(self, divisor, percentage):
        words = set(self.get_words_as_strings())
        for word in words:
            if self.words[word].appeared / float(divisor) < percentage / 100.0:
                self.remove_word(word)


class DataSet:

    def __init__(self, positive_filepaths, negative_filepaths):
        self.positive_words = Dictionary('positive')
        self.negative_words = Dictionary('negative')
        self.positive_filepaths = positive_filepaths
        self.negative_filepaths = negative_filepaths
        self.number_of_reviews = len(positive_filepaths) + len(negative_filepaths)

    def remove_words(self, word_list):
        self.negative_words.remove_words(word_list)
        self.positive_words.remove_words(word_list)

    def make_words_from_filepaths(self, n_grams=1):
        self.positive_words.make_words_from_filepaths(self.positive_filepaths, n_grams)
        self.negative_words.make_words_from_filepaths(self.negative_filepaths, n_grams)

    def calculate_popularity(self):
        for word in self.positive_words.values():
            word.calculate_popularity(len(self.positive_filepaths))
        for word in self.negative_words.values():
            word.calculate_popularity(len(self.negative_filepaths))

    def calculate_info_value(self):
        word_set = set()
        word_set.update(self.positive_words.get_words_as_strings())
        word_set.update(self.negative_words.get_words_as_strings())
        for word in word_set:
            total_appeared = self.positive_words.get_appeared(word) + self.negative_words.get_appeared(word)
            self.positive_words.set_info_value(word, total_appeared)
            self.negative_words.set_info_value(word, total_appeared)

    def prune(self, percentage):
        self.positive_words.prune(self.number_of_reviews, percentage)
        self.negative_words.prune(self.number_of_reviews, percentage)

    def evalute_review(self, filepath):
        strings = Dictionary.remove_nonalphanumeric(FileHandler.read_file(filepath)).split()
        self.remove(strings, f.make_list_from_file('./data/stop_words.txt'))
        strings = set(strings)
        positive_value = 0
        for string in strings:
            popularity = self.positive_words.get_popularity(string)
            if popularity > 0:
                positive_value += m.log2(popularity)
            else:
                try:
                    if string == 'downloading':
                      print('Did not find word:', string, 'in positive reviews')
                except:
                    pass
        negative_value = 0
        for string in strings:
            popularity = self.negative_words.get_popularity(string)
            if popularity > 0:
                negative_value += m.log2(popularity)
        if positive_value > negative_value:
            #print('File:', filepath, '|Positive:', positive_value, '|Negative:', negative_value, '|Conclusion: NEGATIVE')
            return 'negative'
        else:
            #print('File:', filepath, '|Positive:', positive_value, '|Negative:', negative_value, '|Conclusion: POSITIVE')
            return 'positive'

    @staticmethod
    def remove(list, word_list):
        return [x for x in list if x not in word_list]


if __name__ == '__main__':
    f = FileHandler()
    stop_words = f.make_list_from_file('./data/stop_words.txt')
    positive_filepaths = f.make_filepath_list('./data/subset/train/pos/')
    negative_filepaths = f.make_filepath_list('./data/subset/train/neg/')

    data = DataSet(positive_filepaths, negative_filepaths)
    data.make_words_from_filepaths(n_grams=1)
    data.remove_words(stop_words)
    data.prune(1)
    data.calculate_popularity()
    #data.calculate_info_value()

    print("Setup completed!")
    """most_positive = sorted(data.positive_words.values(), reverse=True)[:25]
    most_negative = sorted(data.negative_words.values(), reverse=True)[:25]
    print('          NEGATIVE                                                                                  POSITIVE')
    for i in range(len(most_negative)):
        print(most_negative[i].__repr__(), most_positive[i].__repr__())
    """

    print('Testing negatives...')
    negatives = 0
    positives = 0
    filepaths = f.make_filepath_list('./data/subset/test/neg/')
    for filepath in filepaths:
        if data.evalute_review(filepath) == 'positive':
            positives += 1
        else:
            negatives += 1
    print('Positives:', positives)
    print('Negatives:', negatives)
    print('Correct:', str((negatives/len(filepaths) * 100)) + '%')


    print('Testing positives...')
    negatives = 0
    positives = 0
    filepaths = f.make_filepath_list('./data/subset/test/pos/')
    for filepath in filepaths:
        if data.evalute_review(filepath) == 'positive':
            positives += 1
        else:
            negatives += 1
    print('Positives:', positives)
    print('Negatives:', negatives)
    print('Correct:', str((positives/len(filepaths) * 100)) + '%')

