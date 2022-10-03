"""
        Ngrams Program1
        ---------------

        Author:
            Nebil Weber
            Zach Allen

        NetID:
            nxw180009
            zma180000

        Class:
            CS 4395.001 - Human Language Technologies - F22
        """

# Library Imports
import pickle
from nltk import word_tokenize
from nltk import ngrams
import os
import sys


def readFile(filepath):
    """
               Function to process data and to create unigram and bigram dictionary.

               Args:
                   filepath: one of the 3 training files

               Returns:
                   The unigram dictionary and bigram dictionary from the function
               """

    raw_text = ''

    fp = sys.argv[1]
    filepath = fp
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    raw_text = text_in

    formattedList = ''.join(raw_text.splitlines())  # removes new lines from text
    formattedString = str(formattedList)

    unigram = word_tokenize(formattedString)        # creates unigram list
    bigram = list(ngrams(unigram, 2))               # creates bigram list

    unigram_dict = {t: unigram.count(t) for t in set(unigram)}  # unigram dict
    bigram_dict = {b: bigram.count(b) for b in set(bigram)}  # bigram dict
    return unigram_dict, bigram_dict


# run main functions 3x with the appropriate sys arg
def main():
    """
               This is the main function that builds separate language models for 3 languages.

               Args:
                   One of the 3 training files:
                        LangId.train.English:
                        LangId.train.French
                        LangId.train.Italian

               Returns:
                   None, the program pickles the 6 dictionaries, and saves them to files with appropriate names.
               """

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        unigram_dict, bigram_dict = readFile(fp)

    # save the pickle file "Change language according to the sys arg"
    pickle.dump(unigram_dict, open('Italian_unigram_dict.p', 'wb'))  # write binary

    # save the pickle file "Change language according to the sys arg"
    pickle.dump(bigram_dict, open('Italian_bigram_dict.p', 'wb'))  # write binary


if __name__ == '__main__':
    main()
