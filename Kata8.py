####THESE ARE A BUNCH OF LEVEL 8 KATAS I DID FROM CODEWARS####

#Twice as old - make a function that takes in two numbers one bigger than the other, double the smaller number and subtract it from the larger number
def twice_as_old(dadsAge, sonsAge):
    return abs(dadsAge - sonsAge *2)

#Are You Playing Banjo? - make a function that returns one thing if the input string starts with an "R" and another if it doesn't
def areYouPlayingBanjo(name):
    return name + " plays banjo" if name[0] in ('R','r') else name + " does not play banjo"

areYouPlayingBanjo('rick') #works
areYouPlayingBanjo('tom') #works

##Best method
def areYouPlayingBanjo(name):
    return name + (' plays' if name[0].lower() == 'r' else ' does not play') + " banjo"

#Student's Final Grade - Take input of exam grade and projects finished and return a final class grade
def final_grade(exam, projects):
    if exam > 90 or projects > 10:
        return 100
    elif exam > 75 and projects >= 5:
        return 90
    elif exam > 50 and projects >= 2:
        return 75
    else:
        return 0

# best method
def final_grade(exam, projects):
  if exam > 90 or  projects > 10: return 100
  if exam > 75 and projects >= 5: return 90
  if exam > 50 and projects >= 2: return 75
  return 0

# Barking mad -
class Dog():
    def __init__(self, breed):
        self.breed = breed

    def bark(self):
        return "Woof"

# Best method
class Dog():
  def __init__(self, breed):
    self.breed = breed
    self.bark = lambda: "Woof"

# No zeros for heros - remove trailing zeroes from numbers
def no_boring_zeros(n):
    if n != 0:
        n_string = str(n)
        n_string = n_string.rstrip("0")
        return int(n_string)
    else:
        return 0

#best method
def no_boring_zeros(n):
    try:
        return int(str(n).rstrip('0'))
    except ValueError:
        return 0

# Keep Hydrated! -  we're gonna build a function that returns 1/2 of an input value and then rounds that number down
def litres(time):
    return int(0.5 * time)

#best method
def litres(time):
    return time // 2

# Abbreviate a Two Word Name -  convert a name into initials
def abbrevName(name):
    return ".".join(x[0].upper() for x in name.split(" ") if x)

# Grasshopper - Summation -  finds the summation of every number from 1 to num. The number will always be a positive integer greater than 0
def summation(num):
    sum = 0
    while num > 0:
        sum += num
        num = num - 1
    return sum

# best method
def summation(num):
    return sum(xrange(num + 1))

# Closest elevator - select the closest elevator to a given floor

def elevator(left, right, call):
    return 'right' if abs(right - call) <= abs(left - call) else 'left'

# Filter out the geese - take a list of strings and remove all that exist in a given list
geese = ["African", "Roman Tufted", "Toulouse", "Pilgrim", "Steinbacher"]

def goose_filter(birds):
    return [x for x in birds if x not in geese]

# Get the mean of an array - return the average of a given list
import math
def get_average(marks):
    return math.floor(sum(marks)/len(marks))

# Thinkful - Logic Drills: Traffic light - create a function that returns the next value given an initial color of the
# traffic light

def update_light(current):
    lightsettings = ["green", "yellow", "red"]
    return lightsettings[(lightsettings.index(current) + 1) % 3]

# Check the exam - check that two lists match, for each matching item get 4 points, for non-match get -1 point,
# blank answers get 0 points, if score is <0 return 0
def check_exam(arr1,arr2):
    score = 0
    for i in range(0,len(arr1)):
        if arr2[i] == "":
            continue
        elif arr1[i] == arr2[i]:
            score += 4
        else:
            score += -1
    return score if score>=0 else 0

# best method
def check_exam(arr1, arr2):
    return max(0, sum(4 if a == b else -1 for a, b in zip(arr1, arr2) if b))

# noobCode 01:SUPERSIZE ME....or rather,this integer - given an integer, rearrange the digits to make the biggest
# number possible
def super_size(n):
    return int("".join(sorted(list(str(n)),reverse=True)))