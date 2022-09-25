"""
        Word Guess Game
        ---------------

        Author:
            Nebil Weber

        NetID:
            nxw180009

        Class:
            CS 4395.001 - Human Language Technologies - F22
        """

# imports
import pathlib
import sys
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import random


# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('averaged_perceptron_tagger')


def preprocess_raw_text(rawText):
    """
           The Function processes raw text to applicable format

           Args:
               rawText: input txt file as raw text.

           Returns:
               tokens and a list of 50 common nouns
           """

    # lower case, reduce to only alpha (not in NLTK stopword list), and have length > 5
    token1 = [t.lower() for t in word_tokenize(rawText) if t.isalpha() and t not in stopwords.words('english')
              and len(t) > 5]

    # lemmatize the tokens
    lemma = WordNetLemmatizer()
    lemmas = [lemma.lemmatize(t) for t in token1]

    # get unique lemmas
    lemmaSet = set(lemmas)

    # Pos tag the unique lemmas and print the first 20 tagged lemmas
    tags = nltk.pos_tag(lemmaSet)

    print("\n####################################################################")
    print("##########################", " Question 3 #############################")
    print("####################################################################")
    print("3.c) The first 20 tagged unique lemmas are:\n\t", tags[:20])

    # list of all the noun tags
    list_of_nouns = ['NN', 'NNS', 'NNP', 'NNPS']

    # Create a list of lemmas that are noun Lemmas
    nounLemmas = list([x[0] for x in tags if x[1] in list_of_nouns])

    print("\n3.b)  The number of tokens that are alpha, not in the NLTK stopword list, and have length > 5 is ",
          len(token1))
    # number of noun tags
    print("\n3.d  The number of nounLemmas is ", len(nounLemmas))

    return token1, nounLemmas


def gameTime(topNouns):
    """
              Guessing game Function

              Args:
                  mostly common nouns list of size 50

              Returns:
                  no returns. The game will specify if a player has won or not
              """

    print("\n####################################################################################")
    print("##########################", " Starting the guessing game #############################")
    print("####################################################################################")

    # Print the instructions for the game
    print("\nLet's play a word guessing game!"
          "\n\n Instructions: "
          " You will start by having 5 points."
          " Each correct guess will increase your points."
          " Each wrong guess will decrease your points."
          "\n\t\t\t\tDuplicate guesses won't affect your score."
          " The game will end if your points reaches -1."
          " To end the game, simply "
          "\n\t\t\t\tenter '!' as a guess.\n")

    score = 5                            # initial score
    guessWord = random.choice(topNouns)  # assign the random guess word to be guessed
    letterInput = ''                     # user input
    wordList = []                        # list of guesses from the user

    # create and print the empty dashes
    underscoreSpace = []
    for i in range(len(guessWord)):
        underscoreSpace.append('-')

    print(*underscoreSpace)

    # play until user quits or wins the game
    while True:
        # quit if user wants too
        if letterInput == '!':
            print("\nThank you for playing!")
            sys.exit(0)

        # list to modify guessWord when inserting the guesses to "underscoreSpace"
        gWord = []
        guessList = []
        gWord[:0] = guessWord

        while True:
            # check if user lost
            if score <= -1:
                print("You have lost the game. The secrete word was:",
                      guessWord)

                userInput = input('\nDo you want to play again? (y/n)').lower()

                # replay the game
                if userInput == "y":
                    gameTime(topNouns)

                else:
                    print("\nThank you for playing!")
                    exit(0)

            # check if user wins
            if guessWord == "".join(underscoreSpace):
                print("\nCongrats, you won!!!")
                print("\nTerminating the Program")
                quit()

            # get input letter from the user
            letterInput = input('\n\nPlease guess a letter: ').lower()

            # verify the input
            if not letterInput.isalpha() and not letterInput == "!":
                print("Invalid letter, try again.")

            # break if valid input
            else:
                break

        # check if the user quit the game
        if letterInput == "!":
            print("\nThank you for playing!")
            exit(0)

        # check if the letter is in guessWord
        if letterInput in guessWord:
            for i, j in enumerate(gWord):
                # replace '-' with correct guess letter
                if j == letterInput:
                    underscoreSpace[i] = letterInput

            # make sure same letter is not used
            if letterInput not in wordList:
                print("\nRight guess!")

                # update score
                score = score + 1

                # print score
                print(*underscoreSpace)
                print("Current score = ", score)

                # add letter to guess list
                wordList.append(letterInput)

            # letter is already guesses
            else:
                print("The letter is already chosen.")

        # incorrect guess
        else:
            print("\nSorry, guess again.")
            score = score - 1
            print("Current score = ", score)

    pass


# run main (Starting method of the program)
if __name__ == '__main__':
    # print error if no argument was passed and abort the program.
    if len(sys.argv) < 2:
        print('Please enter a anat19.txt file as system arg')
        quit()
    else:
        # store the argument file
        data_file = sys.argv[1]

        # validate the file name
        if not (data_file.__eq__("anat19.txt")):
            print("Error with the data file. Aborting the program.")
            quit()

    # open file for reading
    with open(pathlib.Path.cwd().joinpath(data_file), 'r') as f:

        # read the first line and remove it
        data = f.read()
        f.close()

    # Word_tokenize the data and get the unique tokens
    tokens = [t.lower() for t in word_tokenize(data)]
    tokens_set = set(tokens)

    print("\n####################################################################")
    print("##########################", " Question 2 #############################")
    print("####################################################################")
    # lexical diversity
    print("\t\t\t\t\tLexical diversity: %.2f" % (len(tokens_set) / len(tokens)))

    # process the token and save results
    tokens1, nouns = preprocess_raw_text(data)

    # Create a dictionary of all the nouns and their count
    nouns_dict = {}
    for noun in nouns:
        nouns_dict[noun] = tokens1.count(noun)

    # Stores 50 most common nouns
    mostCommonNoun = []
    counter = 1

    print("\n####################################################################")
    print("##########################", " Question 4 #############################")
    print("####################################################################")
    print("The 50 most common words and their counts are: ")

    # Print the 50 most common nouns and their count
    for noun in sorted(nouns_dict, key=nouns_dict.get, reverse=True)[:50]:
        print(counter, "-> ", noun, ':', nouns_dict[noun])
        mostCommonNoun += [noun]
        counter = counter + 1

    # Initialize the game!!!!!!
    gameTime(mostCommonNoun)
