#!/usr/bin/python
import sys, re
from functools import reduce

DEBUG = False
#DEBUG = True

# Put prios between 0 and 100. Above 100 is for default strategy
MAXNPRIO = 200    # max number of prios, 0 is lowest prio
FALLBACKPRIO = MAXNPRIO    # max number of prios, 0 is lowest prio
prios = [(i, []) for i in range(MAXNPRIO + 1)]


def outputPrios(goalLines, lemma):
    rankedGoals = [str(goal) + "\n" for prioList in prios for goal in prioList[1]]
    print("".join(rankedGoals))


def dumpPrios(goalLines, lemma):
    print("Prios:")
    for pl in prios:
        for p in pl[1]:
            print("    > level:{}, goalNo:{}".format(pl[0], p))


def prioritize(goalNumber, prio, goalLine):
    prios[prio][1].insert(0, goalNumber)
    if DEBUG:
        goal = re.sub("\s+", " ", goalLine)
        print("goalNo:{} prio:{} goal:{}".format(goalNumber, prio, goal))


def genPrios(goalLines, lemma):
    # Prioritize splitEqs over new instances
    splitEqs = False
    splitEqsLine = -1
    for i in range(len(goalLines)):
        if re.match(".*splitEqs.*", goalLines[i]):
            splitEqs = True
            splitEqsLine = i

    for line in goalLines:
        goal = line.split(':')[0]
        if "sanity" in lemma:
            if DEBUG:
                print("MATCHING Sanity LEMMA: {}".format(lemma))
            if re.match(".*aeadEncrypt.*", line) or\
               re.match(".*xorEncrypt.*", line):
                    prioritize(goal, 80, line)
            else:
                prioritize(goal, 50, line)
        elif "secrecy" in lemma or\
             "helpInvLtkKDF" in lemma or\
             "helpInvKeyDep" in lemma:
            if DEBUG:
                print("MATCHING Secrecy LEMMA: {}".format(lemma))
            if re.match(".*KU\( ~ltk.*", line) or\
                 re.match(".*KU\( ~xx.*", line) or\
                 re.match(".*KU\( ~yy.*", line) or\
                 re.match(".*KU\( 'g'\^\(~xx\*~yy\).*", line) or\
                 re.match(".*KU\( 'g'\^\(~ltk\*~(xx|yy)\).*", line):
                    prioritize(goal, 90, line)
            elif re.match(".*StI.*", line) or\
               re.match(".*StR.*", line) or\
               re.match(".*LTKRev.*", line) or\
               re.match(".*aeadEncrypt.*", line) or\
               re.match(".*xorEncrypt.*", line) or\
               re.match(".*sign.*", line):
                    prioritize(goal, 80, line)
            elif re.match(".*KU\( hkdfExtract.*", line) or\
                 re.match(".*KU\( hkdfExpand.*", line):
                    prioritize(goal, 75, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 70, line)
            else:
                 prioritize(goal, 50, line)
        elif "helpInvLtk" in lemma:
            if DEBUG:
                print("MATCHING helpInvLtk LEMMA: {}".format(lemma))
            elif re.match(".*aeadEncrypt.*", line) or\
                 re.match(".*xorEncrypt.*", line):
                    prioritize(goal, 90, line)
            elif re.match(".*KU\( hkdfExtract.*", line) or\
                 re.match(".*KU\( hkdfExpand.*", line):
                    prioritize(goal, 75, line)
            else:
                prioritize(goal, 50, line)
        else:
            if DEBUG:
                print("NO MATCH FOR LEMMA: {}".format(lemma))
            exit(0)


def echoOracle(goalLines, lemma):
    for line in goalLines:
        goal = line.split(':')[0]
        prioritize(goal, 0, line)

def testMatch(pattern, tamarinString):
    if re.match(pattern, tamarinString):
        print("Matches!")
    else:
        print("Don't match!")

if __name__ == "__main__":
    if sys.argv[1] == "testMatch":
        if len(sys.argv) != 4:
            print("usage: oracle.py testMatch pattern tamarinString")
            sys.exit(1)
        testMatch(sys.argv[2], sys.argv[3])
        sys.exit(0)

    goalLines = sys.stdin.readlines()
    lemma = sys.argv[1]

    genPrios(goalLines, lemma)
    #echoOracle(goalLines, lemma)

    # We want 0 to be lowest prio, so reverse all level-lists and the list itself
    prios = [(p[0], p[1][::-1]) for p in prios][::-1]

    outputPrios(goalLines, lemma)
    #dumpPrios(goalLines, lemma)



