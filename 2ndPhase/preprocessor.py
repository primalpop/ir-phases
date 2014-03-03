#!/usr/bin/python

"""
calcwts

Homework 2: http://www.csee.umbc.edu/~nicholas/676/term%20project/hw2.html

Author: Primal Pappachan, primal1@umbc.edu

"""
import nltk, unicodedata, HTMLParser
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
    html_parser = HTMLParser.HTMLParser()
    f = open(filename)
    raw = f.read()
    cleaned = nltk.clean_html(raw)     
    cleaned = cleaned.decode('utf8', 'ignore')
    cleaned = html_parser.unescape(cleaned)
    cleaned = unicodedata.normalize('NFKD', cleaned).encode('latin-1','ignore')
    return cleaned

def tokenizer(cleaned):
    """
        Converts cleaned text to a vocabulary.
        Returns dictionary.
    """
    tokenizer = nltk.tokenize.RegexpTokenizer("[\w’]+", flags=re.UNICODE)
    text = tokenizer.tokenize(cleaned)
    words = [w.lower() for w in text if len(w) > 2]
    #Stopwords removal
    stopwords = open('stoplist.txt').read().splitlines() #from file
    # try:
    #     stopwords.extend(nltk.corpus.stopwords.words('english')) #from nltk corpus
    # except Exception:
    #     pass   
    words = [word for word in words if word not in stopwords]    
    return words

def write_to_file(output, filename, output_path):
    """
        Writes into an output file.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    outfile = output_path + filename[-8:-5] + '.txt'
    with open(outfile, "w") as f:
        f.write(output)
    return

if __name__ == "__main__":
    
    try:
        input_path = sys.argv[1] #Path to input directory
        output_path = sys.argv[2] #Path to output directory
        number_of_files = eval(sys.argv[3]) #Number of files
        if not output_path.endswith('/'): output_path = output_path + '/' #Checks and adds trailing slash to output directory
    
    except:
        print "Missing Parameters"
        print "Usage: python preprocessor.py files out_files <n>"
        print "<n> - Number of files, n = [1, 503]"
        sys.exit(1)    
        
    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for filename in filenames:
            list_of_files.append(os.sep.join([dirpath, filename])) #List of complete files
    #random.shuffle(list_of_files) #Randomizing the order of files in the list
    
    model = collections.defaultdict(dict) #document : term : frequency
    for i in range(0, number_of_files): # Slicing the list of files as per Number of files
        filename = list_of_files[i]
        cleaned = clean_html(filename) #cleaning raw html string
        tokens = tokenizer(cleaned) #tokenization
        for token in tokens:
            model[filename][token] = freq(token, tokens)

    for i in range(0, number_of_files):
        doc = list_of_files[i]
        output = ""
        for word in model[doc].keys():
            output += "%s \t %s \n" %(word, tf_idf(model, word, doc))
        write_to_file(output, doc, output_path)     
        