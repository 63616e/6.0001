# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
            self.message_text = text 
            self.valid_words = load_words(WORDLIST_FILENAME)
        
        

    def get_message_text(self):
         return self.message_text

    def get_valid_words(self):
        copy = self.valid_words.copy()
        return copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        if shift < 0 or shift > 26:
            raise ValueError("Shift must be between 0 and 26")
        else:
            return {letter: chr(ord('a') + (ord(letter) + shift - ord('a') % 26) % 26) for letter in string.ascii_lowercase}
        
        

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        if shift < 0 or shift > 26:
            raise ValueError("Shift must be between 0 and 26")
        else:
            return ''.join([self.build_shift_dict(shift)[letter] for letter in self.message_text])
        

class PlaintextMessage(Message):
    def __init__(self, text, shift):
            self.message_text = text
            self.valid_words  = load_words(WORDLIST_FILENAME)
            self.shift = shift
            self.encryption_dict = self.build_shift_dict(shift)
            self.message_text_encrypted = self.apply_shift(shift)

       
        

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        copy = self.encryption_dict.copy()
        return copy

    def get_message_text_encrypted(self):
        
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text): 
            self.message_text= text 
            self.valid_words = load_words(WORDLIST_FILENAME)
        
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift = 0
        best_shift_decrypted = ''
        best_shift_count = 0
        for shift in range(26):
            decrypted_text = self.apply_shift(shift)
            decrypted_text_list = decrypted_text.split(' ')
            count = 0
            for word in decrypted_text_list:
                if is_word(self.valid_words, word):
                    count += 1
            if count > best_shift_count:
                best_shift_count = count
                best_shift = shift
                best_shift_decrypted = decrypted_text
        return (best_shift, best_shift_decrypted)

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
   plaintext = PlaintextMessage('hello', 2)
   print('Expected Output: jgnnq')
   print('Actual Output:', plaintext.get_message_text_encrypted())
   ciphertext = CiphertextMessage('jgnnq')
   print('Expected Output:', (24, 'hello'))
   print('Actual Output:', ciphertext.decrypt_message())