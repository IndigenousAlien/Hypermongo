import re

def checkNum(name1):
    return any(i.isdigit() for i in name1)

def newName(ylabel):
    changeName = re.compile("([a-zA-Z]+)([0-9]+)")
    for i in range(0,4):
        tempName = ylabel[i]
        if checkNum(tempName) == True:
            tempName = changeName.match(tempName).groups()
            tempName = "r'$" + tempName[0] + "_{" + tempName[1] + "}$'"
        ylabel[i] = tempName
    return ylabel 

name1 ="m1"
name2 = "m2"
name3 = "eccentricity"
name4 = "x2"
ylabel = [name1, name2, name3, name4]
ylabel = newName(ylabel)

print (ylabel[0])