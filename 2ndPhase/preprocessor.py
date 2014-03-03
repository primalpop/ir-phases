__author__ = 'Primal Pappachan'
#coding: utf8

"""
Pre-Processor

Homework 2: http://www.csee.umbc.edu/~nicholas/676/term%20project/hw2.html

Author: Primal Pappachan, primal1@umbc.edu

"""

import nltk, unicodedata
import os, sys, re
import collections
import random, math

def freq(tok, tokens):
    return tokens.count(tok)

def tf(term_freq, total_freq):
    return term_freq / float (total_freq)

def idf(N, word, vocabulary):
    """
        N - Total number of documents
        vocabulary - Complete list of tokens
    """
    #import ipdb; ipdb.set_trace()
    return math.log(N / float(freq(word, vocabulary)))

def tf_idf(model, word, doc):
    """
        model - document : word : frequency
    """
    vocabulary = []
    for docs in model.values():
        vocabulary.extend(docs.keys()) # for computing document frequency in idf
    #import ipdb; ipdb.set_trace()
    term_freq = model[doc][word]   
    total_freq = sum(model[doc].values()) #for normalizing in tf
    N = len(model.keys())
    tf_value = tf(term_freq, total_freq)
    idf_value = idf(N, word, vocabulary) 
    return tf_value * idf_value 

def bm_25():
    pass                 

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
    return cleaned

def tokenizer(cleaned):
    """
        Converts cleaned text to a vocabulary.
        Returns dictionary.
    """
    text = nltk.word_tokenize(cleaned)
    words = [w.lower() for w in text]
    #Stopwords check and deletion
    stopwords = open('stoplist.txt').read().splitlines()
    words = [word for word in words if word not in stopwords]

    new_vocab = []
    for word in words:
        if re.search(r'^\d+\.\d+', word) or not re.search(r'^\W+$', word) or re.search(r'^\w+', word):
            new_vocab.append(word)
    
    return new_vocab

def write_to_file(model, filename, output_path):
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

if __name__ == "__main__":
    
    try:
        input_path = sys.argv[1] #Path to input directory
        output_path = sys.argv[2] #Path to output directory
        number_of_files = eval(sys.argv[3]) #Number of files
        if not output_path.endswith('/'): output_path = output_path + '/' #Checks and adds trailing slash to output directory
    
    except:
        print "Missing Parameters"
        print "Usage: python tokenize.py files out_files <n>"
        print "<n> - Number of files, n = [1, 503]"
        sys.exit(1)    
        
    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for filename in filenames:
            list_of_files.append(os.sep.join([dirpath, filename])) #List of complete files
    #random.shuffle(list_of_files) #Randomizing the order of files in the list
    
    model = collections.defaultdict(dict) #document : term : frequency
    for i in xrange(0, number_of_files): # Slicing the list of files as per Number of files
        filename = list_of_files[i]
        cleaned = clean_html(filename) #cleaning raw html string
        tokens = tokenizer(cleaned) #tokenization
        for token in tokens:
            model[filename][token] = freq(token, tokens)

    print tf_idf(model, 'mexican', '../input_files/001.html')        
        