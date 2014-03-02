__author__ = 'primpap'
#coding: utf8

#Ref: http://www.nltk.org/book/ch03.html
#Ref: http://stackoverflow.com/questions/2922783/how-do-you-walk-through-the-directories-using-python

import nltk
import os, sys, re
from collections import Counter
import random

full_vocab = {}
sorted_dir = 'sorted_files/'
token_dir = 'token_files/'

def clean_html(filename):
    f = open(filename)
    raw = f.read()
    cleaned = nltk.clean_html(raw)

    # replace special strings
    special_characters = {
        '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
        '&lt;'   : '<', '&gt;'  : '>', '&eacute;' : 'e',
        '&#146;' : ''
    }

    for (k,v) in special_characters.items():
        cleaned = cleaned.replace (k, v)

    re.sub(r'\W+', '', cleaned)
    cleaned = cleaned.lower()

    return cleaned

def tokenizer(cleaned, filename):

    tokens = nltk.wordpunct_tokenize(cleaned)
    #print type(tokens)
    #print tokens
    text = nltk.Text(tokens)
    #print type(text)

    words = [w.lower() for w in text]
    vocab = sorted(words)

    new_vocab = []

    for word in vocab:
        if not re.search(r'^\W+$', word) or re.search(r'^\w+', word):
            new_vocab.append(word)

    #print type(new_vocab), len(new_vocab)  #new_vocab

    new_vocab_dict = {}

    for (word, freq) in Counter(new_vocab).iteritems():
        new_vocab_dict[word] = freq

    #full_vocab.update(new_vocab_dict)
    #write_token_file(new_vocab_dict, filename)
    return





def write_token_file(vocab, filename):
    outfile = token_dir + filename[-8:-5] + '.txt'
    for (word, freq) in vocab.iteritems():
        with open(outfile, "a") as f:
            #print ('%s :: %s' % (word, freq))
            f.write('%s  %s \n' % (word, freq))
    return


def word_sort():
    with open(sorted_dir + 'sorted_by_tokens.txt', "w") as f:
        for k in sorted(full_vocab):
            f.write('%s  %s \n' % (k, full_vocab[k]))
    return


def freq_sort():
    with open(sorted_dir + 'sorted_by_freq.txt', "w") as f:
        for word in sorted(full_vocab.iteritems(), key=lambda(k, v): (-v, k)):
            f.write('%s  %s \n' % (word[0], full_vocab[word[0]]))
    return


if __name__ == "__main__":
    path = sys.argv[1]
    number_of_files = eval(sys.argv[2])
    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            list_of_files.append(os.sep.join([dirpath, filename]))

    random.shuffle(list_of_files)
    #print list_of_files
    for i in xrange(0, number_of_files):
        filename = list_of_files[i]
        cleaned = clean_html(filename)
        tokenizer(cleaned, filename)

    #word_sort()
    #freq_sort()