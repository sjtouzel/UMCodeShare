# find the odd or even standout in a list of numbers
def iq_test(numbers):
    testnumslist = numbers.split() # split the string of numbers into a list of strings
    testnumslist = [int(i) for i in testnumslist] # convert the strings to int type
    odds = [x for x in testnumslist if x%2!=0] # create a list of odd numbers
    evens = [x for x in testnumslist if x%2==0] # create a list of even numbers
    return testnumslist.index(odds[0]) + 1 if len(odds)<len(evens) else testnumslist.index(evens[0]) + 1 # return the
                    # index (plus 1) of the single odd or even number in the list

int.index(evens[0]) + 1

# Best Method
def iq_test(numbers):
    e = [int(i) % 2 == 0 for i in numbers.split()] # Create a list of true for even numbers and false for odd numbers

    return e.index(True) + 1 if e.count(True) == 1 else e.index(False) + 1 # return the index plus 1 of the true item
                # in the list if there's only one, otherwise return the index plus one of the false item

# Take a string and remove a subset of letters and then re-assemble the string as a sentence

def song_decoder(song):
    wordList = []
    for str in song.split("WUB"):
        print(str, 1)
        wordList.append(str)
    while '' in wordList:
        wordList.remove('')
    return " ".join(wordList) # join all the words back together but remove the empties

def song_decoder(song):
    return " ".join(x for x in song.split("WUB") if x) # This will return a string with all of the WUBs removed and
                                                # since it checks that x exists it won't return any extra whitespace

# Best Method
def song_decoder(song):
    return " ".join(song.replace('WUB', ' ').split())

song_decoder("WUBWEWUBAREWUBWUBTHEWUBCHAMPIONSWUBMYWUBFRIENDWUB")

# Let's make a function that will find all the words in a string that are 5 letters or longer and then turn them backwards

def spin_words(string): # first we'll create a function that checks each word and reverses the big ones
    wordList = [] # create an empty list to hold our edited words
    for str in string.split(): # split our input string by spaces
        if len(str) >= 5: # check each one for length
            newword = [] # create an empty list to hold our rearranged letters
            for n in range(0, len(str)): # rearrange the letters
                newword.insert(0,str[n]) # put each new letter at the beginning of the list
            wordList.append("".join(newword)) # combine the letters and append to our list of words
        else:
            wordList.append(str) # if the word is shorter, then just append to the list of words as is
    return " ".join(wordList) # join all the words back together

spin_words("I love Hambone")

# Best method
def spin_words(sentence):
    return " ".join([x[::-1] if len(x) >= 5 else x for x in sentence.split(" ")])

# make a function that takes a string and returns the string with every other letter capitalized
def to_weird_case(string):
    if " " in string: # check for spaces in the string, then we'll have to split it up
        newStrings = string.split() # this will create an array of each word in the string
        wordList = [] # This array will hold all of our updated case words
        for n in newStrings:
            letterList = []
            for b in range(0, len(n)):
                if b % 2 == 0:
                    letterList.append(n[b].upper()) # add an uppercase version of every odd letter in the string to the array
                else:
                    letterList.append(n[b].lower()) # for every other letter just add a lower case version
            wordList.append(''.join(letterList))  # use the ''.join() to create the fixed up word
        return ' '.join(wordList) # use the ' '.join() to recreate the string with spaces
    else:
        letterList = []
        for n in range(0, len(string)):
            if n % 2 == 0:
                letterList.append(string[n].upper()) # add an uppercase version of every odd letter in the string to the array
            else:
                letterList.append(string[n].lower()) # for every other letter just add a lower case version
        return ''.join(letterList) # use the ''.join() to create the fixed up word


# Best Method - uses two functions to first correct each word and then to join each word
def to_weird_case_word(string):
    return "".join(c.upper() if i % 2 == 0 else c for i, c in enumerate(string.lower()))


def to_weird_case(string):
    return " ".join(to_weird_case_word(str) for str in string.split())

# make sure you get back to your starting point after 10 steps
def isValidWalk(walk):
    directionDictionary = {'n':1,'e':12,'w':-12,'s':-1 } # create a dictionary that changes values to numbers
    if len(walk) == 10: # make sure there's at least 10 turns so you go for exactly 10 minutes
        count = [] # create an empty array for the numbers
        for n in walk: # convert the letters to numbers
            count.append(directionDictionary[n])
        print(count)
        print (sum(count))
        if sum(count) == 0: # if they sum to 0 then you'll come back to the starting point and the walk is good
            return True
        else:
            return False # if you don't pass those criteria, the walk is no good

# Best method
def isValidWalk(walk):
    return len(walk) == 10 and walk.count('n') == walk.count('s') and walk.count('e') == walk.count('w')

# Check two arrays to make sure each number in the second array is the square of a number in the first array
def comp(a1,a2):
    print(a1,a2)
    if a2 is None: # check that a2 is not null
        return False
    elif not a1 and not a2:  # if both arrays are empty that's ok
        return True
    for n in a1: # check to make sure each value has a square
        if n*n in a2:
            continue
        else:
            return False
    for n in a2: # check to make sure each value has a square root
        if n**0.5 in a1:
            continue
        else:
            return False
    return True # all qualifications passed? mark it true

# best method
def comp(array1, array2):
    try:
        return sorted([i ** 2 for i in array1]) == sorted(array2) # first sort each array then test that each value matches
    except: # everything else returns false
        return False

# look for the single odd or even number in an array
def find_outlier(intArray):
    evenCount = 0
    evenNum = 0
    oddCount = 0
    oddNum = 0
    for n in range(0,len(intArray)):
        if intArray[n] % 2 == 0:
            evenCount += 1
            evenNum = intArray[n]
        else:
            oddCount += 1
            oddNum = intArray[n]
    if evenCount < 2:
        return evenNum
    elif oddCount < 2:
        return oddNum

# best method
def find_outlier(int):
    odds = [x for x in int if x%2!=0]
    evens= [x for x in int if x%2==0]
    return odds[0] if len(odds)<len(evens) else evens[0]

# build a function that parses out a long spaceless string into individual real words
VALID_WORDS = ['good', 'luck']

def max_match(sentence): # this shit works but apparently it needs to go faster
    wordList = [] # create a list to hold all the words or letters
    if sentence in VALID_WORDS: # if the string is a word already
        wordList.append(sentence) # add is to the word list
    else: # if it's not in the word list we do this to find the longest word and iterate through the whole sentence
        testSentence = sentence
        while len(testSentence) != 1: # while the word is longer than one letter do the following
            if testSentence in VALID_WORDS: # check to make sure the new word isn't in the set
                wordList.append(testSentence)
                testSentence = ''
                break
            else: # if the new word isn't in the set
                for n in range(1,len(testSentence)):
                    if len(testSentence)-n == 1: #if it's the last letter to test
                        wordList.append(testSentence[0]) # we append the letter to the wordList
                        testSentence = testSentence[-n:]  # and start the process over with what's left over
                        break
                    elif testSentence[:-n] in VALID_WORDS: # remove the last letter from the string and see if the string is a word
                        wordList.append(testSentence[:-n]) # if it is, add it to the word list
                        testSentence = testSentence[-n:] # and start the process over with what's left over
                        break
                    else:
                        continue
        if len(testSentence) > 0:
            wordList.append(testSentence[0])
    return wordList

#second attempt
def max_match(sentence):
    wordList = []  # create a list to hold all the words or letters
    # check the first 12 characters only, then rebuild the string with the left overs and grab the next 12 character stretch








zipp = "butts"
zipp[:-1]
testing = 'handkerchief'
len(testing)
testing.split(3)

n=5
[testing[i:i+n] for i in range(0,len(testing),n)]