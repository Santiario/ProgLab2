__author__ = 'keithd'

# A subset of prims1.py used for projects in TDT-4113

from inspect import isfunction # Need this to test whether something is a function!

# The reduce function was removed in Python 3.0, so just use this handmade version.  Same as a curry.
def kd_reduce(func,seq):
    res = seq[0]
    for item in seq[1:]:
        res = func(res,item)
    return res

# Returns n versions of either a number or string, or the result of calling the same function n times.
def n_of(count, item):
    if isfunction(item):
        return [item() for i in range(count)]
    else:
        return [item for i in range(count)]

# Calculate the frequency of occurrence of every character in a file, whose pathname is the argument 'fid'.
def calc_char_freqs(fid):
    "Create a dictionary with pairs (char : freq) based on the entire file"
    return gen_freqs(lowercase_chars_from_file(fid))

def gen_freqs(items):
    " Creates a dictionary of pairs (item : frequency)"
    fc = {}
    for item in items:
        if item in fc.keys():
            fc[item] = fc[item] + 1
        else:
            fc[item] = 1
    size = len(items)
    for key in fc.keys():
        fc[key] = fc[key]/size
    return fc

def lowercase_chars_from_file(fid):
    return [c.lower() for c in strings_explode(load_file_lines(fid))]

# Loads in all lines of a file
def load_file_lines(fid):
    return [line.rstrip() for line in open(fid, 'r').readlines()]
    # rstrip strips the newline character.

def string_explode(s):
    "Generate a list of characters (singleton strings) from a string"
    items = []
    for i in range(len(s)):
        items.append(s[i])
    return items

def strings_explode(strings):
    "Returns one huge list of all the exploded strings"
    items = []
    for s in strings:
        items.extend(string_explode(s))
    return items

def n_strings(count,base,gap=''):
    " Create n copies of the same string, with the string 'gap' between each copy"
    return merge_strings(n_of(count,base),gap=gap)

def merge_strings(strings, gap=' '):
        return kd_reduce((lambda x, y: x + gap + y), strings)