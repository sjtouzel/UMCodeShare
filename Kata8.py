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