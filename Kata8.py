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

summation(5)