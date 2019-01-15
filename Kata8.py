####THESE ARE A BUNCH OF LEVEL 8 KATAS I DID FROM CODEWARS####

#make a function that takes in two numbers one bigger than the other, double the smaller number and subtract it from the larger number
def twice_as_old(dadsAge, sonsAge):
    return abs(dadsAge - sonsAge *2)

#make a function that returns one thing if the input string starts with an "R" and another if it doesn't
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