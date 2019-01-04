# Check an array as if it were a tic tac toe board
def isSolved(board):
    # Check each row for a straight set
    for n in board:
        if all(x==n[0] for x in n): # check if the row is all one number
            if n[0]==0: # if it's zero that's not a win
                continue
            else:
                return n[0]
    # Check each column for a straight set
    columns = []  # empty list for the columns
    for n in range(0, 3):  # arrange the numbers in each list to be the columns instead of rows
        columns.append([item[n] for item in board])
    for n in columns:
        if all(x==n[0] for x in n): # check if the columns contains a straight set
            if n[0]==0:
                continue
            else:
                return n[0]
    # Check the diagonals
    diagonals = [[board[0][0],board[1][1],board[2][2]],[board[0][2],board[1][1],board[2][0]]]
    for n in diagonals:
        if all(x==n[0] for x in n): # check if the lists contains a straight set
            if n[0]==0:
                continue
            else:
                return n[0]
    # check if game is unfinished or a cat
    allrowslist = []
    for n in board:
        for b in n:
            allrowslist.append(b)
    return -1 if 0 in allrowslist else 0

# Best Method
def isSolved(board):
    for i in range(0, 3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][0]

    elif 0 not in board[0] and 0 not in board[1] and 0 not in board[2]:
        return 0
    else:
        return -1

# take a list of numbers and Order them by the sum of the digits
def order_weight(string):  # THIS ONE DIDN'T WORK CAUSE DICTIONARIES CAN'T HAVE DUPLICATE KEYS
    listofweights = string.split() # split the string of weights into individual strings
    dictionaryofweights = {} # create an empty dictionary to hold our weights and digit sums
    for n in listofweights: # attach the weights and digit sums as keys and values in the dictionary
        sumofdigits = 0
        for b in range(0,len(n)):
            sumofdigits += int(n[b])
        dictionaryofweights[sumofdigits] = n
    sortedweightsdict = sorted(dictionaryofweights.items(), key=lambda x: x[0]) # sort the dictionary based on
                                                                                # the sum of digits
    sortedweights = [] # create an empty list to hold the rearranged weights
    for t in sortedweightsdict: # append the sorted weights
        sortedweights.append(t[1])
    return " ".join(sortedweights) # Return a string of the sorted weights

def order_weight(string): # THIS ONE WORKED
    listofweights = string.split()  # split the string of weights into individual strings
    arrayofweightswithsums = [] # create an empty list to hold our weights and digit sums
    for n in listofweights: # attach the weights and digit sums as sub lists in the big list
        sumofdigits = 0
        for b in range(0, len(n)): # create the sums
            sumofdigits += int(n[b])
        entryarray = [sumofdigits, n] # Here's the sub list
        arrayofweightswithsums.append(entryarray)  # Now attach the list to the big list
    sortedweightswithsums = sorted(arrayofweightswithsums) # sort the list
    return " ".join(el[1] for el in sortedweightswithsums) # Return a string of the sorted weights

# Best method
def order_weight(_str):
    return ' '.join(sorted((_str.split(' ')), key=lambda x: sum(int(c) for c in x)))

order_weight("123 867 123 498 783")

# Build a function that counts the size of a loop made with nodes
def loop_size(node):
    count = 0 # This is an empty counter that will hold the index of our last node in the loop
    listOfNodes = [] # this list will contain each node item we read through
    nodeWork = node # begin with the first node
    while nodeWork not in listOfNodes: # loop through each node until you come to a match in the list
        listOfNodes.append(nodeWork) # add the current node to the list
        nodeWork = nodeWork.next # move to the next node
        count += 1 # increase the counter by 1 until we reach a match
    # listOfNodes.append(nodeWork)
    # indexList = [i for i, e in enumerate(listOfNodes) if e == nodeWork]
    return count-listOfNodes.index(nodeWork) # subtract the index of the beginning of our loop from the end of the loop

# Best Method
def loop_size(node):
    turtle, rabbit = node.next, node.next.next

    # Find a point in the loop.  Any point will do!
    # Since the rabbit moves faster than the turtle
    # and the kata guarantees a loop, the rabbit will
    # eventually catch up with the turtle.
    while turtle != rabbit:
        turtle = turtle.next
        rabbit = rabbit.next.next

    # The turtle and rabbit are now on the same node,
    # but we know that node is in a loop.  So now we
    # keep the turtle motionless and move the rabbit
    # until it finds the turtle again, counting the
    # nodes the rabbit visits in the mean time.
    count = 1
    rabbit = rabbit.next
    while turtle != rabbit:
        count += 1
        rabbit = rabbit.next

    # voila
    return count


# Create a Class and give it some class functions to help tell you what's inside the class item

class PaginationHelper(object):

    # The constructor takes in an array of items and an integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        # First set all universal variables to the "self." objects
        self.collection = collection
        self.items_per_page = items_per_page
        self.collection_page_split = []
        # lets create a bunch of lists for each page of items
        while len(collection) > items_per_page:
            page_list = collection[:items_per_page]
            self.collection_page_split.append(page_list)
            collection = collection[items_per_page:]
        self.collection_page_split.append(collection)


    # returns the number of items within the entire collection
    def item_count(self):
        return len(self.collection)

    # returns the number of pages
    def page_count(self):
        return len(self.collection_page_split) # count the number of lists to find out how many pages we have

    # returns the number of items on the current page. page_index is zero based
    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        return len(self.collection_page_split[page_index]) if page_index in range(0,len(self.collection_page_split)) else -1


    # determines what page an item is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        if len(self.collection) == 0: # if the collection is empty return -1
            return -1
        elif item_index == 0: # gotta get the zero index out so we can test for even division values and put them on the right page
            return 0
        elif 0 < item_index < len(self.collection): # get the page to look on and subtract one if it's an even division value
            if item_index % self.items_per_page == 0:
                return item_index / self.items_per_page - 1
            else:
                return item_index / self.items_per_page
        else:
            return -1

# Best Method

class PaginationHelper:

    # The constructor takes in an array of items and a integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        self.collection = collection
        self.items_per_page = items_per_page

    # returns the number of items within the entire collection
    def item_count(self):
        return len(self.collection)

    # returns the number of pages
    def page_count(self):
        if len(self.collection) % self.items_per_page == 0:
            return len(self.collection) / self.items_per_page
        else:
            return len(self.collection) / self.items_per_page + 1

    # returns the number of items on the current page. page_index is zero based
    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        if page_index >= self.page_count():
            return -1
        elif page_index == self.page_count() - 1:
            return len(self.collection) % self.items_per_page or self.items_per_page
        else:
            return self.items_per_page

    # determines what page an item is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        if item_index >= len(self.collection) or item_index < 0:
            return -1
        else:
            return item_index / self.items_per_page

# Create a couple functions that will convert text to base64 and base64 to text
def to_base_64(string):
    # we use the encode value to take a string to base64 format
    bayce64eq = string.encode('base64').replace('\n', '') # encode adds some extra shit we need to get rid of
    return bayce64eq.replace('=', '') # we also gotta remove the extra '=' signs too


def from_base_64(string):
    a = string
    if len(a) % 4 == 0: # if it's divisible by 4 then the decode will work
        return a.decode('base64')
    else:
        while len(a) % 4 != 0: # if not we gotta add some '=' signs till the string is divisible by 4
            a = a + '='
        return a.decode('base64')

# Best Method
tobase64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
frombase64 = {v: i for i, v in enumerate(tobase64)} # create a dictionary
for counter, value in enumerate(tobase64):
    print(counter, value)


def to_base_64(string):
    padding = (3 - len(string) % 3) % 3
    if padding != 0:
        string += chr(0) * padding
    base64 = ''
    for i in xrange(0, len(string), 3):
        code = (ord(string[i]) << 16) + (ord(string[i + 1]) << 8) + ord(string[i + 2])
        base64 += tobase64[(code >> 18) % 64] + tobase64[(code >> 12) % 64] + tobase64[(code >> 6) % 64] + tobase64[
            code % 64]
    if padding > 0:
        base64 = base64[:-padding]
    return base64


def from_base_64(string):
    padding = (4 - len(string) % 4) % 4
    if padding != 0:
        string += 'A' * padding
    str = ''
    for i in xrange(0, len(string), 4):
        code = (frombase64[string[i]] << 18) + (frombase64[string[i + 1]] << 12) + (frombase64[string[i + 2]] << 6) + \
               frombase64[string[i + 3]]
        str += chr((code >> 16) % 256) + chr((code >> 8) % 256) + chr(code % 256)
    if padding > 0:
        str = str[:-padding]
    return str

# Build an ROT13 decoder - ROT13 is a code that splits the alphabet in half and then stacks the two halves to find the
# code value for the given letter

message = "EBG13 \n rknzcyr"

def rot13(message):
    print(message)
    top =    "{}`[]@():ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 123456789.,?!'"
    bottom = "{}`[]@():NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm 123456789.,?!'"
    # split the input and output strings into lists
    toplist = list(top)
    toplist.append('\n')
    bottomlist = list(bottom)
    bottomlist.append('\n')
    # Create the dictionary by combining those two lists
    translatedict = dict(zip(toplist, bottomlist))
    # split the message into a list of letters and symbols
    messagelist = list(message)
    # use the dictionary to translate the code
    translation = [translatedict[i] for i in messagelist]
    return ''.join(translation)

# Best Method
def rot13(message):
  return message.encode('rot13')

# Build Functions that do what they say. ex. five(plus(two())) will return 7
def zero(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '0')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 0
def one(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '1')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 1
def two(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '2')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 2
def three(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '3')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 3
def four(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '4')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 4
def five(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '5')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 5
def six(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '6')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 6
def seven(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '7')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 7
def eight(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '8')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 8
def nine(*args):
    if args:
        if args[0] == "BUTTS":
            return 0
        else:
            doingmath = args[0]
            doingmath.insert(0, '9')
            usewithEval = " ".join(doingmath)
            return eval(usewithEval)
    else:
        return 9

def plus(number):
    addlist = ['+', str(number)]
    return addlist
def minus(number):
    sublist = ['-', str(number)]
    return sublist
def times(number):
    multiplyList = ['*',str(number)]
    return multiplyList
def divided_by(number):
    if number == 0:
        return "BUTTS"
    else:
        divideByList = ['//', str(number)] # use // operator to return integers instead of float. it'll round down
        return divideByList

# BEST METHOD
def zero(f = None): return 0 if not f else f(0) # if there is nothing passed to zero() then return 0.
                                                # if there is something passed to it put 0 into the child function
def one(f = None): return 1 if not f else f(1)
def two(f = None): return 2 if not f else f(2)
def three(f = None): return 3 if not f else f(3)
def four(f = None): return 4 if not f else f(4)
def five(f = None): return 5 if not f else f(5)
def six(f = None): return 6 if not f else f(6)
def seven(f = None): return 7 if not f else f(7)
def eight(f = None): return 8 if not f else f(8)
def nine(f = None): return 9 if not f else f(9)

def plus(y): return lambda x: x+y # take the input value and build a partial function to pass to the parent function
def minus(y): return lambda x: x-y
def times(y): return lambda  x: x*y
def divided_by(y): return lambda  x: x/y

# build a function that reads a line of input and performs tasks based on string values
def simple_assembler(program):
    register = {}
    counter = 0
    while (counter < len(program)):
        getcommand = program[counter] # grab each command one at a time
        commandsplit = getcommand.split() # split the command into parts
        if commandsplit[0] == 'mov': # check for the 'mov' type of command
            register[commandsplit[1]] = register[commandsplit[2]] if commandsplit[2].isalpha() \
                else int(commandsplit[2])# set the dictionary value to the other key value or the number
        elif commandsplit[0] == 'inc': # check for the 'inc' type of command
            register[commandsplit[1]] += 1
        elif commandsplit[0] == 'dec': # check for the 'dec' type of command
            register[commandsplit[1]] -= 1
        elif commandsplit[0] == 'jnz' and register[commandsplit[1]] if \
                commandsplit[1].isalpha() else int(commandsplit[1]): # check for the 'jnz' type of command
            # Try this one instead: condition = register[cell] if cell.isalpha() else int(cell)
            if commandsplit[2].isalpha():
                counter += register[commandsplit[2]]
            else:
                counter += int(commandsplit[2]) - 1
        counter += 1
    return register

# BEST METHOD
allRs = []
def simple_assembler(program):
    d, i = {}, 0 # set up your empty dictionary and counter
    while i < len(program): # run each code till you get to the end of the program
        cmd, r, v = (program[i] + ' 0').split()[:3] # split the command into 3 parts
        allRs.append(r)
        if cmd == 'inc':
            d[r] += 1
        if cmd == 'dec':
            d[r] -= 1
        if cmd == 'mov':
            d[r] = d[v] if v in d else int(v)
        if cmd == 'jnz' and (d[r] if r in d else int(r)): # this will make sure the r value exists in the library
            # and that it is not 0 (zero). It acts as boolean test. Anything that is in the library and
            # not zero will return True and execute the next step.
            i += int(v) - 1
        i += 1
    return d

# build a function that will find the max sum of a contiguous subsequence in an array or list of integers
# return 0 if all the numbers are negative
def maxSequence(arr):
    if not arr: # check for empty array
        return 0
    elif all(x < 0 for x in arr): # check for all negative array
        return 0
    elif all(x > 0 for x in arr): # sum an array of all positives
        return sum(arr)
    else:
        highestSumArray = [max(arr)] # use this sub array to hold the best collection, we'll start it out with
                                     # the highest value in the input array
        for i in range(0,len(arr)):
            testArray = [arr[i]]  # use this sub array to hold the test selection
            counter = i+1
            while counter < len(arr): # now incrementally add consecutive values to the array until we reach the end of
                                      # the array. if we get a summed value higher than the highestSumArray, replace the
                                      # highestSumArray with the testArray, and continue testing
                testArray.append(arr[counter])
                if sum(testArray) <= sum(highestSumArray):
                    counter += 1
                else:
                    highestSumArray = testArray[:] # gotta use the [:] when copying shit cause python sets a reference
                                                   # to the variable being copied and will update each list as it goes
                    counter += 1
        return sum(highestSumArray)

# BEST METHOD
def maxSequence(arr):
    max,curr=0,0
    for x in arr:
        curr+=x
        if curr<0:curr=0
        if curr>max:max=curr
    return max
