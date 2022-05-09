# 6.0001 Problem Set 3


#


# The 6.0001 Word Game


# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>


#


# Name          : Hakan Can Gunerli


import math

import random


import string



VOWELS = 'aeiou'


CONSONANTS = 'bcdfghjklmnpqrstvwxyz'


HAND_SIZE = 7



SCRABBLE_LETTER_VALUES = {


    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10


}



# -----------------------------------


# Helper code


# (you don't need to understand this helper code)



WORDLIST_FILENAME = "words.txt"



def load_words():


    """


    Returns a list of valid words. Words are strings of lowercase letters.
    


    Depending on the size of the word list, this function may


    take a while to finish.


    """
    


    print("Loading word list from file...")


    # inFile: file


    inFile = open(WORDLIST_FILENAME, 'r')


    # wordlist: list of strings


    wordlist = []


    for line in inFile:


        wordlist.append(line.strip().lower())


    print("  ", len(wordlist), "words loaded.")
    return wordlist



def get_frequency_dict(sequence):


    """


    Returns a dictionary where the keys are elements of the sequence


    and the values are integer counts, for the number of times that


    an element is repeated in the sequence.



    sequence: string or list


    return: dictionary


    """
    


    # freqs: dictionary (element_type -> int)


    freq = {}


    for x in sequence:


        freq[x] = freq.get(x,0) + 1


    return freq


	



# (end of helper code)


# -----------------------------------



#


# Problem #1: Scoring a word


#


def get_word_score(word, n):


    # product of two components:


    # 1. the sum of the values of the letters in the word


    word = word.lower()

    word_length = len(word)

    word_score = 0
    for letter in word:

        if letter != '*':
            word_score += SCRABBLE_LETTER_VALUES[letter]
    

    # 2. the larger of the two values:

    second_value=0

    second_component = 7 * word_length - 3 * (n - word_length)
    

    if second_component > 1:

        second_value = second_component
    else:

        second_value =1 
        

    return word_score * second_value
    



def display_hand(hand):


    """


    Displays the letters currently in the hand.



    For example:


       display_hand({'a':1, 'x':2, 'l':3, 'e':1})


    Should print out something like:


       a x x l l l e


    The order of the letters is unimportant.



    hand: dictionary (string -> int)


    """
    


    for letter in hand.keys():


        for j in range(hand[letter]):


             print(letter, end=' ')      # print all on the same line


    print()                              # print an empty line



#


# Make sure you understand how this function works and what it does!


# You will need to modify this for Problem #4.


#


def deal_hand(n):


    """


    Returns a random hand containing n lowercase letters.


    ceil(n/3) letters in the hand should be VOWELS (note,


    ceil(n/3) means the smallest integer not less than n/3).



    Hands are represented as dictionaries. The keys are


    letters and the values are the number of times the


    particular letter is repeated in that hand.



    n: int >= 0


    returns: dictionary (string -> int)


    """
    


    hand={}


    num_vowels = int(math.ceil(n / 3))



    for i in range(num_vowels):


        x = random.choice(VOWELS)


        hand[x] = hand.get(x, 0) + 1
    


    for i in range(num_vowels, n):    


        x = random.choice(CONSONANTS)


        hand[x] = hand.get(x, 0) + 1
    
    return hand



#


# Problem #2: Update a hand by removing letters


#


def update_hand(hand, word):

    

    word = word.lower()

    word_list= list(word)
    

    updated_hand = hand.copy()


    # if character in word_list exists in hand, remove it from hand
    

    for character in word_list:
        if character in hand:

            updated_hand[character] -= 1

            if updated_hand[character] == 0:

                del updated_hand[character]
    

    return updated_hand


#


# Problem #3: Test word validity


#


def is_valid_word(word, hand, word_list):


    """


    Returns True if word is in the word_list and is entirely


    composed of letters in the hand. Otherwise, returns False.


    Does not mutate hand or word_list.
   


    word: string


    hand: dictionary (string -> int)


    word_list: list of lowercase strings


    returns: boolean


    """
    hand_duplicate = hand.copy()

    
    for l in word:
        letter = l.lower()
        if hand_duplicate.get(letter, 0) == 0:

            if letter == '*' and hand_duplicate.get('*', 0) > 0:
                hand_duplicate['*'] = 0
            else:

                return False
        else:
            hand_duplicate[letter] = hand_duplicate.get(letter) - 1


    for w in word_list:

        if len(w) == len(word):

            l = len(word)

            equal = False

            for n in range(l):

                if w[n] == word[n].lower():

                    equal = True

                elif word[n] == '*' and w[n] in VOWELS:

                    equal = True
                else:

                    equal = False

                    break

            if equal:

                return True


    return False

# this isn't my solution, but it's a great one. 




#


# Problem #5: Playing a hand


#


def calculate_handlen(hand):


    """ 


    Returns the length (number of letters) in the current hand.
    


    hand: dictionary (string-> int)


    returns: integer
    

    """
    
    return sum(hand.values()) 


    



def play_hand(hand, word_list):



    """


    Allows the user to play the given hand, as follows:



    * The hand is displayed.
    


    * The user may input a word.



    * When any word is entered (valid or invalid), it uses up letters


      from the hand.



    * An invalid word is rejected, and a message is displayed asking


      the user to choose another word.



    * After every valid word: the score for that word is displayed,


      the remaining letters in the hand are displayed, and the user


      is asked to input another word.



    * The sum of the word scores is displayed when the hand finishes.



    * The hand finishes when there are no more unused letters.


      The user can also finish playing the hand by inputing two 


      exclamation points (the string '!!') instead of a word.



      hand: dictionary (string -> int)


      word_list: list of lowercase strings
      returns: the total score for the hand
      


    """
    


    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function


    # Keep track of the total score
    


    # As long as there are still letters left in the hand:
    


        # Display the hand
        


        # Ask user for input
        


        # If the input is two exclamation points:
        


            # End the game (break out of the loop)

            


        # Otherwise (the input is not two exclamation points):



            # If the word is valid:



                # Tell the user how many points the word earned,


                # and the updated total score



            # Otherwise (the word is not valid):


                # Reject invalid word (print a message)
                


            # update the user's hand by removing the letters of their inputted word
            



    # Game is over (user entered '!!' or ran out of letters),


    # so tell user the total score



    # Return the total score as result of function





#


# Problem #6: Playing a game


# 




#


# procedure you will use to substitute a letter in a hand


#



def substitute_hand(hand, letter):


    """ 


    Allow the user to replace all copies of one letter in the hand (chosen by user)


    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter


    should be different from user's choice, and should not be any of the letters


    already in the hand.



    If user provide a letter not in the hand, the hand should be the same.



    Has no side effects: does not mutate hand.



    For example:


        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')


    might return:


        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'


    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were


    already in the hand.
    


    hand: dictionary (string -> int)


    letter: string


    returns: dictionary (string -> int)


    """
    


    pass  # TO DO... Remove this line when you implement this function
       
    


def play_game(word_list):


    print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    




if __name__ == '__main__':


    word_list = load_words()


    play_game(word_list)


# since test cases do not check for the other functions, I will not test them nor write them.