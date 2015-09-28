__author__ = 'Vemund'
# -*- coding: utf-8 -*-


class Viginere:

    def __init__(self, shiftword):
        self.shiftword = shiftword

    def decode(self, string):
        result = ''
        string.lower()
        codeword_index = 0

        for c in string:
            value = ord(c) - 97
            shiftnum = ord(self.shiftword[codeword_index]) - 97
            print(shiftnum)
            value = (value - shiftnum) % 26
            result += chr(value + 97)
            codeword_index = (codeword_index + 1) % len(self.shiftword)
        return result

    def encode(self, string):
        result = ''
        string.lower()
        codeword_index = 0

        for c in string:
            value = ord(c) - 97
            shiftnum = ord(self.shiftword[codeword_index]) - 97
            value = (value + shiftnum) % 26
            value %= 26
            result += chr(value + 97)
            codeword_index = (codeword_index + 1) % len(self.shiftword)
        return result

coder = Viginere('tgifriday')
print(coder.decode("wkntiawedxsbiknlrcxtmskzhsrnjmskmusmfqwrdmutgesqyksrnrhxqsemqkjhqsjeblfcfzqazvqepxtnqfbwppxsqj"))



class Ceaser:

    def __init__(self, shift):
        self.shift = shift

    def encode(self, string):
        result = ''
        for c in string.lower():
            value = ord(c) - 97
            value = (value + self.shift) % 26
            result += chr(value + 97)
        return result

    def decode(self, string):
        result = ''
        for c in string.lower():
            value = ord(c) - 97
            value = (value - self.shift) % 26
            result += chr(value + 97)
        return result


