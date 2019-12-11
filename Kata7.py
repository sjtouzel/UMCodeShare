# Palindrome creator - this will take an input number then add the reverse version of that
    # number to it until the result is a palindrome, it'll then tell you how many times it took to get a palindrome
def palindrome_chain_length(number):
    backwardsnum = [] # create an empty array for our rearranged number
    for n in range(0, len(str(number))): # Re-sort the input number with the last number first
        backwardsnum.insert(0,str(number)[n])
    backwardsnum = int("".join(backwardsnum)) # change the backwardsnum array back into an int type
    count = 0 # start the count of times it takes to find a palindrome
    while number != backwardsnum: # test the new number and then repeat the reversing and testing till we find a palindrome
        count +=1 # this will keep count of how many times we have to try the process
        number = backwardsnum + number
        backwardsnum = []
        for n in range(0, len(str(number))):
            backwardsnum.insert(0, str(number)[n])
        backwardsnum = int("".join(backwardsnum))
    return count

# Best Method
def palindrome_chain_length(n):
    steps = 0
    while str(n) != str(n)[::-1]:
        n = n + int(str(n)[::-1])
        steps += 1
    return steps

palindrome_chain_length(47)
47 +74

# Get the Middle Character - This function will find and return the middle letter or letters from a given string
def get_middle(s):
    stringLength = len(s)
    if stringLength % 2 == 0:
        middle = stringLength/2
        return s[middle-1:middle+1]
    else:
        middle=stringLength/2
        return s[middle]

    #your code here

# best method
def get_middle(s):
   return s[(len(s)-1)/2:len(s)/2+1]

# Given two numbers, sum all of the integers between those numbers (inclusive)
import numpy as np
def get_sum(a,b):
    sortList = (a,b)
    a = min(sortList)
    b = max(sortList)
    listToSum = np.arange(a, (b+1))
    return sum(listToSum)

get_sum(-3,18)
get_sum(-1,2)
get_sum(4,4)
get_sum(-1,-1)
get_sum(0,0)

# best method
def get_sum(a,b):
    return sum(range(min(a,b), max(a,b)+1))

# Count the number of vowels in a string
def getCount(inputStr):
    num_vowels = 0
    # your code here
    for n in range(0, len(inputStr)): # get the length of the string to iterate through each letter
        if inputStr[n] in ("a", "e", "i", "o", "u"): # if the letter is in this list add one to our count
            num_vowels += 1
        else: # if it's anything else, test the next letter
            continue
    return num_vowels # return the count
getCount("hambone")

# best method
def getCount(inputStr):
    return sum(1 for let in inputStr if let in "aeiouAEIOU")

import math
def is_square(n):
    if n < 0: # This will check to make sure its a positive number
        return False
        #print ("%s is not a square number") %n
    elif math.sqrt(n).is_integer(): # this will check each positive number to make sure the square root is an integer
        return True
        #print ("%s is a square number") %n
    else: # everything else is not a perfect square
        return False
        #print ("%s is not a square number") % n

# Extended weekends - Find the first and last month in a range of years that have 5 weekends and count how many months have 5 weekends in the range
import calendar #has all the relevant data for the months of the year
# Find months that have 5 fridays, saturdays, and sundays in a given year
jan2019 = calendar.monthcalendar(2019,1) # this will write out the days of a given month January 2019, weeks start with monday
####Apparently this shit takes too long. times out on codewars. must optimize. Couldn't get it to run fast enough
def solve(begYear, endYear):
    extendedMonthsList = []
    for i in list(range(begYear,endYear+1)): #check each year
        for n in list(range(1,13)): #check each month
            yearmonthCombo = [i,n]
            yearmonthTest = calendar.monthcalendar(yearmonthCombo[0],yearmonthCombo[1]) # get the list of days for that month
            monthWeekends = [] #create empty list to contain the weekend values from the calender
            for p in yearmonthTest: #populate the list of weekend values
                monthWeekends.append(p[4:])
            monthWeekendsList = [item for sublist in monthWeekends for item in sublist]  # convert the list of lists to a single list
            if monthWeekendsList[0] is 1 and monthWeekendsList[-1] is 31:
                extendedMonthsList.append(yearmonthCombo[1])
            else:
                continue
    return calendar.month_abbr[extendedMonthsList[0]], calendar.month_abbr[extendedMonthsList[-1]], len(
        extendedMonthsList)

### apparently this shit here is way faster:
from calendar import month_abbr
from datetime import datetime
def solve(a,b):
    res = [month_abbr[month]
    for year in range(a, b+1)
    for month in [1,3,5,7,8,10,12]
    if datetime(year, month, 1).weekday() == 4]
    return res[0],res[-1], len(res)


# Digital cypher vol 2 - create a function that will decode a numerical representation of letters into words given a key value
import string
def decode(code, key):
    decoded = [] # create an empty list to hold all the decoded letters
    letterDict = dict(zip(range(1,27), string.ascii_lowercase))# establish the dictionary, numbers to be converted to letters
    #convert the key to a string so we can access each number to subtract from our code
    strKey = str(key)
    #repeat the string for the entire length of the code
    newKey = (strKey * ((len(code) // len(strKey)) + 1))[:len(code)]
    #Iterate through the code values
    for i in range(0,len(code)):
        decoded.append(letterDict.get(code[i] - int(newKey[i])))
    #now rejoin the decoded letters and return it
    return ''.join(decoded)

#best method
def decode(code, key):
    key = str(key)
    return "".join([chr(code[i] + 96 - int(key[i % len(key)])) for i in range(0, len(code))])


# The Hotel with Infinite Rooms - make a formula that spits out how many people are staying in a hotel on a given day
def group_size(S, D):  ####This shit is too slow
    while D > 0:
        D = D - S
        S += 1
    return S - 1

##Whatever the fuck this is man...
from math import floor
def group_size(S, D):
    return floor((2*D+S*(S-1))**.5+.5)

# Ranking position - The challenge is sort by points and calulate position for every person. But remember if two or more
#  persons have same number of points, they should have same position number and sorted by name (name is unique)

def ranking(people):
    sortedPeople = sorted(people, key=lambda i: (-i['points'], i['name']))
    for i in range(0,len(sortedPeople)):
        if i == 0:
            sortedPeople[i].update({"position": i + 1})
        elif sortedPeople[i].get('points') == sortedPeople[i-1].get('points'):
            sortedPeople[i].update({"position":sortedPeople[i-1].get('position')})
        else:
            sortedPeople[i].update({"position": i + 1})
    return sortedPeople

# Simple Fun #2: Circle of Numbers - given a total number and a starting number find the number directly opposite
# of the starting numbers given that the numbers are equally spaced around a circle

def circle_of_numbers(n, fst):
    halfTotal = n/2
    oppoNum = fst + halfTotal
    return oppoNum if oppoNum < n else oppoNum - n

# best method

def circle_of_numbers(n, fst):
    return (fst + (n/2)) % n

# After(?) Midnight - take a negative or positive integer which represents the number of minutes before or after
# sunday at midnight and return the current day of the week and the current time in 24hr format ('hh:mm') as a string
# ex. input = 45 returns 'Sunday 00:45'

import math
import calendar
def day_and_time(mins):
    day = calendar.day_name[int(math.fmod(6 + math.fmod((int(math.floor(mins/ 1440))), 7),7))]
    if mins >= 0:
        hours = str((mins//60) % 24).zfill(2)
        mins = str(mins % 60).zfill(2)
        time = hours + ':' + mins
    else:
        hours = str(24 - abs(mins//60) % 24).zfill(2)
        mins = str(mins % 60).zfill(2)
        time = hours + ':' + mins
    return day + ' ' + time

# best method
from datetime import timedelta, datetime
def day_and_time(mins):
    return "{:%A %H:%M}".format(datetime(2017, 1, 1) + timedelta(minutes = mins))

# Principal Diagonal | VS | Secondary Diagonal - add up the values of the two diagonals and return whichever one is larger
def diagonal(matrix):
    primdiag = 0
    secdiag = 0
    for i in range(0,len(matrix[0])):
        primdiag += matrix[i][i]
        secdiag += matrix[i][len(matrix)-1-i]
    if primdiag == secdiag:
        return "Draw!"
    else:
        return "Principal Diagonal win!" if primdiag>secdiag else "Secondary Diagonal win!"

# best method
def diagonal(matrix):
    sp, ss = map(sum, zip(*((matrix[x][x], matrix[len(matrix)-1-x][x]) for x in range(len(matrix)))))
    return "Draw!" if ss == sp else "{} Diagonal win!".format("Principal" if sp > ss else "Secondary")

# Functional Addition - Create a function add(n) which returns a function that always adds n to any number
    # create a function that returns a function
def add(n):
    def additionfun(x):
        return x + n
    return additionfun

addone = add(1) # this will pass a function to addone, that will add 1 to whatever number we pass to addone()
addone(4)

#best method
def add(n):
    return lambda x: x + n

# Unlucky Days - Calculate how many Friday 13th's there are in a given year
from datetime import date
def unlucky_days(year):
    daycount = 0
    for i in range(1,13):
        dayof13 = date(year,i,13).weekday() # get the weekday for each 13th day of each month
        if dayof13 == 4: #
            daycount += 1
    return daycount

#best method
from datetime import date
def unlucky_days(year):
    return sum(date(year, m, 13).weekday() == 4 for m in range(1, 13))

# Spinning Rings - find when two counts match up when one counts up and the other counts down
# 0123 vs 0321, while both start counting at 0
def spinning_rings(inner_max, outer_max):
    outerlist = list(range(0,outer_max + 1))
    innerlist = list(range(inner_max, -1, -1))
    innerlist.insert(0,innerlist.pop(len(innerlist)-1))
    spincount = 1
    innernum = innerlist[spincount]
    outernum = outerlist[spincount]
    while innernum != outernum:
        spincount += 1
        innernum = innerlist[spincount % (len(innerlist))]
        outernum = outerlist[spincount % (len(outerlist))]
    return spincount

#best method
from itertools import count

def spinning_rings(inner_max, outer_max):
    return next(i for i in count(1) if i % (outer_max + 1) == -i % (inner_max + 1))


# How many arguments - write a function that returns a count of the number of arguments passed into it
def args_count(*args,**kwargs):
    return len(args) + len(kwargs)

# Alphabetical Addition - write a function that takes letter inputs and converts them to their number equivalent
# add those numbers together and then convert the sum back into a letter
def add_letters(*letters):
    LETTERS = {letter: index for index, letter in enumerate(list(map(chr, range(97, 123))), start=1)}
    lettersSum = 0
    for i in letters:
        lettersSum += LETTERS.get(i)
    print(lettersSum)
    divtest = divmod(lettersSum,26)
    print(divtest)
    if divtest[1] != 0:
        return chr(divtest[1]+96)
    else:
        return chr(122)

# Best Method
def add_letters(*letters):
    return chr( (sum(ord(c)-96 for c in letters)-1)%26 + 97)
