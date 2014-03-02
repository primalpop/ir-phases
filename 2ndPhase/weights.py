__author__ = 'Primal Pappachan'
#coding: utf8

"""
Homework 2: http://www.csee.umbc.edu/~nicholas/676/term%20project/hw2.html

Author: Primal Pappachan, primal1@umbc.edu

"""

import nltk
import os, sys, re
from collections import Counter
import random
import unicodedata

sorted_dir = 'sorted_files/' #Path to directory of files sorted by tokens and frequency
token_dir = 'token_files/' #Path to directory of individual token files corresponding to input files

def update_dictionary(full_dict, new_dict):
    """
        Joins two dictionaries. Joins new_dict to  full_dict and returns full_dict.
    """
    for word in new_dict.keys():
        if full_dict.has_key(word):
            full_dict[word] += new_dict[word]
        else:
            full_dict[word] = new_dict[word]
    return full_dict        

def clean_html(filename):
    """
        Clean the raw string read from Input Document. 
        It removes the html markup, formatting as well as non alphanumeric characters.
        Return string. 
    """
    f = open(filename)
    raw = f.read()
    cleaned = nltk.clean_html(raw) 
    
    cleaned = cleaned.decode('utf8', 'ignore')
    cleaned = unicodedata.normalize('NFKD', cleaned).encode('ascii', 'ignore')

    # replace special strings
    special_characters = {
        '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
        '&lt;'   : '<', '&gt;'  : '>', '&eacute;' : 'e',
        '&#146;' : ''
    }

    for (k,v) in special_characters.items():
        cleaned = cleaned.replace (k, v)

    return cleaned

def tokenizer(cleaned, filename, output_path):
    """
        Converts cleaned text to a vocabulary.
        Returns dictionary.
    """
    text = nltk.word_tokenize(cleaned)

    words = [w.lower() for w in text]

    new_vocab = []

    for word in words:
        if re.search(r'^\d+\.\d+', word) or not re.search(r'^\W+$', word) or re.search(r'^\w+', word):
            new_vocab.append(word)

    new_vocab_dict = {}

    for (word, freq) in Counter(new_vocab).iteritems():
        new_vocab_dict[word] = freq

    #full_vocab.update(new_vocab_dict) #Updating the Global dictionary
    
    write_token_file(new_vocab_dict, filename, output_path)
    return new_vocab_dict

def write_token_file(vocab, filename, output_path):
    """
        Writes vocabulary into an output file.
    """
    directory = output_path + token_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    outfile = directory + filename[-8:-5] + '.txt'
    for (word, freq) in vocab.iteritems():
        with open(outfile, "a") as f:
            f.write('%s  %s \n' % (word, freq))
    return

def word_sort(output_path, full_vocab):
    """
        Writes vocabulary sorted by tokens into an output file.
    """
    directory = output_path + sorted_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + 'sorted_by_tokens.txt', "w") as f:
        for k in sorted(full_vocab):
            f.write('%s  %s \n' % (k, full_vocab[k]))
    return

def freq_sort(output_path, full_vocab):
    """
        Writes vocabulary sorted by frequency into an output file.
    """
    directory = output_path + sorted_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + 'sorted_by_freq.txt', "w") as f:
        for word in sorted(full_vocab.iteritems(), key=lambda(k, v): (-v, k)):
            f.write('%s  %s \n' % (word[0], full_vocab[word[0]]))
    return

if __name__ == "__main__":
    try:
        input_path = sys.argv[1] #Path to input directory
        output_path = sys.argv[2] #Path to output directory
        number_of_files = eval(sys.argv[3]) #Number of files
        if not output_path.endswith('/'): output_path = output_path + '/' #Checks and adds trailing slash to output directory
        list_of_files = []

        for (dirpath, dirnames, filenames) in os.walk(input_path):
            for filename in filenames:
                list_of_files.append(os.sep.join([dirpath, filename])) #List of complete files

        random.shuffle(list_of_files) #Randomizing the order of files in the list
        
        full_vocab = {} #Global dictionary to store the full vocabulary
        for i in xrange(0, number_of_files): # Slicing the list of files as per Number of files
            filename = list_of_files[i]
            cleaned = clean_html(filename) #cleaning raw html string
            new_vocab = tokenizer(cleaned, filename, output_path) #tokenization
            full_vocab = update_dictionary(full_vocab, new_vocab) #Updating the Global dictionary        

        #Uncomment/Comment following two lines of the code to obtain complete vocabulary sorted by token and frequency to a file    
        word_sort(output_path, full_vocab) #vocabulary sorted by tokens
        freq_sort(output_path, full_vocab) #vocabulary sorted by tokens
    except:
        print "Missing Parameters"
        print "Usage: python tokenize.py files out_files <n>"
        print "<n> - Number of files, n = (0, 503]"
        