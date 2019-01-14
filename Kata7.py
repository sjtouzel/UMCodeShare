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

# This function will find and return the middle letter or letters from a given string
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
    return sum(xrange(min(a,b), max(a,b)+1))

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

# Find the first and last month in a range of years that have 5 weekends and count how many months have 5 weekends in the range
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


# create a function that will decode a numerical representation of letters into words given a key value
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
