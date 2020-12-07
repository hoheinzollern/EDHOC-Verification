#!/usr/bin/python3
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
    # splitEqs = False
    # splitEqsLine = -1
    # for i in range(len(goalLines)):
    #     if re.match(".*splitEqs.*", goalLines[i]):
    #         splitEqs = True
    #         splitEqsLine = i

    for line in goalLines:
        goal = line.split(':')[0]
        if "sanity" in lemma:
            if DEBUG:
                print("MATCHING Sanity LEMMA: {}".format(lemma))
            if re.match(".*SKRev.*", line) or\
               re.match(".*Completed.*", line):
                    prioritize(goal, 90, line)
            elif re.match(".*StR.*", line) or\
               re.match(".*StI.*", line):
                    prioritize(goal, 80, line)
            elif re.match(".*KU\( 'g'\^~xx \).*", line) or\
               re.match(".*KU\( 'g'\^~yy \).*", line) or\
               re.match(".*KU\( ~xx.*", line) or\
               re.match(".*KU\( ~yy.*", line) or\
               re.match(".*~~>.*", line) or\
               re.match(".*=.*=.*", line):
                    prioritize(goal, 70, line)
            elif re.match(".*LTK_.*", line):
                    prioritize(goal, 67, line)
            elif re.match(".*aead.*", line):
                    prioritize(goal, 65, line)
            elif re.match(".*KU\( sign.*", line) or\
               re.match(".*KU\( extr.*", line) or\
               re.match(".*KU\( expa.*", line):
                    prioritize(goal, 60, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 55, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 55, line)
            else:
                prioritize(goal, 50, line)
        elif "authImplicit" in lemma: #"authGIYImplicitAuthGuarantee" in lemma:   # Special for imp agree
            if DEBUG:
                print("MATCHING Auth LEMMA: {}".format(lemma))
            if re.match(".*: !KU\( ~xx \).*", line) or\
                 re.match(".*: !KU\( ~yy \).*", line) or\
                 re.match(".*: !KU\( ~xx\.. \).*", line) or\
                 re.match(".*: !KU\( ~yy\.. \).*", line) or\
                 re.match(".*~~>.*", line) or\
                 re.match(".*: !KU\( 'g'\^~xx \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~xx\.. \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~yy \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~yy\.. \).*", line) or\
                 re.match(".*: !KU\( ~ltk \).*", line) or\
                 re.match(".*: !KU\( ~ltk\.. \).*", line) or\
                 re.match(".*: !KU\( pk\(~ltk\) \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk\.. \).*", line) or\
                 re.match(".*: !LTK_SIG\(.*", line) or\
                 re.match(".*: !LTK_STAT\(.*", line) or\
                 re.match(".*: !PK_SIG\(.*", line) or\
                 re.match(".*: !PK_STAT\(.*", line) or\
                 re.match(".*: StI._.*", line) or\
                 re.match(".*: StR._.*", line) or\
                 re.match(".*ExpRunning.*", line):
                      prioritize(goal, 97, line)
            elif re.match(".*KU\( 'g'\^\(~yy.*\*~ltk.*", line) or\
                 re.match(".*KU\( 'g'\^\(~xx.*\*~ltk.*", line):
                    prioritize(goal, 93, line)
            elif re.match(".*KU\( 'g'\^\(~xx.*\*~yy.*", line) or\
                 re.match(".*KU\( 'g'\^\(~yy.*\*~xx.*", line):
                    prioritize(goal, 90, line)
            elif re.match(".*KU\( extr.*", line) or\
                 re.match(".*KU\( expa.*", line):
                    prioritize(goal, 80, line)
            elif re.match(".*LTKRev.*", line) or\
                 re.match(".*sign.*", line) or\
                 re.match(".*aead.*", line):
                    prioritize(goal, 70, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 60, line)
            elif re.match(".*KU\( \(.V⊕.*", line):
                    prioritize(goal, 40, line)
            else:
                 prioritize(goal, 50, line)
        elif "auth" in lemma:
            if DEBUG:
                print("MATCHING Auth LEMMA: {}".format(lemma))
            if re.match(".*KU\( ~ltk.*", line) or\
               re.match(".*KU\( ~xx.*", line) or\
               re.match(".*KU\( ~yy.*", line):
                    prioritize(goal, 98, line)
            elif re.match(".*: !KU\( ~xx \).*", line) or\
                 re.match(".*: !KU\( ~yy \).*", line) or\
                 re.match(".*: !KU\( ~xx\.. \).*", line) or\
                 re.match(".*: !KU\( ~yy\.. \).*", line) or\
                 re.match(".*~~>.*", line) or\
                 re.match(".*: !KU\( 'g'\^~xx \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~xx\.. \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~yy \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~yy\.. \).*", line) or\
                 re.match(".*: !KU\( ~ltk \).*", line) or\
                 re.match(".*: !KU\( ~ltk\.. \).*", line) or\
                 re.match(".*: !KU\( pk\(~ltk\) \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk\.. \).*", line) or\
                 re.match(".*: !LTK_SIG\(.*", line) or\
                 re.match(".*: !LTK_STAT\(.*", line) or\
                 re.match(".*: !PK_SIG\(.*", line) or\
                 re.match(".*: !PK_STAT\(.*", line) or\
                 re.match(".*: StI._.*", line) or\
                 re.match(".*: StR._.*", line) or\
                 re.match(".*ExpRunning.*", line):
                      prioritize(goal, 90, line)
            elif \
                 re.match(".*aead.*", line) or\
                 re.match(".*KU\( expa.*", line) or\
                 re.match(".*KU\( extr.*", line):
                    prioritize(goal, 87, line)
            elif re.match(".*KU\( 'g'\^~ltk.*\).*", line) or\
                 re.match(".*KU\( 'g'\^\(~ltk.*\).*", line) or\
                 re.match(".*Helper.*", line) or\
                 re.match(".*~~>.*", line) or\
                 re.match(".*=.*=.*", line):
                    prioritize(goal, 85, line)
            elif re.match(".*KU\( 'g'\^\(~yy.*\*~ltk.*", line) or\
                 re.match(".*KU\( 'g'\^\(~xx.*\*~ltk.*", line):
                    prioritize(goal, 80, line)
            elif re.match(".*KU\( 'g'\^\(~xx.*\*~yy.*", line) or\
                 re.match(".*KU\( 'g'\^\(~yy.*\*~xx.*", line):
                    prioritize(goal, 75, line)
            elif re.match(".*LTKRev.*", line) or\
                 re.match(".*sign.*", line) or\
                 re.match(".*splitEqs.*", line) or\
                 re.match(".*StI.*", line) or\
                 re.match(".*StR.*", line):
                    prioritize(goal, 70, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 60, line)
            elif re.match(".*KU\( \(.V⊕.*", line):
                    prioritize(goal, 40, line)
            else:
                 prioritize(goal, 50, line)
        elif "AEAD" in lemma:
            if DEBUG:
                print("MATCHING AEAD LEMMA: {}".format(lemma))
            if re.match(".*: !KU\( ~xx \).*", line) or\
                re.match(".*: !KU\( ~yy \).*", line) or\
                re.match(".*: !KU\( ~xx\.. \).*", line) or\
                re.match(".*: !KU\( ~yy\.. \).*", line) or\
                re.match(".*: !KU\( ~ltk \).*", line) or\
                re.match(".*: !KU\( ~ltk\.. \).*", line) or\
                re.match(".*: !KU\( ~AD_3.*", line):
                    prioritize(goal, 90, line)
            elif \
                re.match(".*KU\( 'g'\^\(~xx\*~yy\).*", line) or\
                re.match(".*KU\( 'g'\^\(~ltk\*~yy\).*", line) or\
                re.match(".*KU\( 'g'\^\(~ltk\*~xx\).*", line):
                    prioritize(goal, 80, line)
            elif \
                re.match(".*: !KU\( *aead\(.*", line) or\
                re.match(".*: !KU\( *expa.*", line):
                re.match(".*: !KU\( *extr.*", line) or\
                    prioritize(goal, 70, line)
            elif \
                 re.match(".*last.*", line) or\
                 re.match(".*: !KU\( pk\(~ltk\) \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk \).*", line) or\
                 re.match(".*: !KU\( 'g'\^~ltk\.. \).*", line) or\
                 re.match(".*: !LTK_SIG\(.*", line) or\
                 re.match(".*: !LTK_STAT\(.*", line) or\
                 re.match(".*: !PK_SIG\(.*", line) or\
                 re.match(".*: !PK_STAT\(.*", line) or\
                 re.match(".*: St.*", line):
                      prioritize(goal, 60, line)
            else:
                prioritize(goal, 50, line)
        elif "secrecy" in lemma:
            if DEBUG:
               print("MATCHING Secrecy LEMMA: {}".format(lemma))
            if re.match(".*KU\( ~ltk.*", line) or\
               re.match(".*KU\( 'g'\^\(~ltk\*.*\).*", line):
                    prioritize(goal, 97, line)
            elif re.match(".*KU\( ~xx.*", line) or\
                 re.match(".*KU\( ~yy.*", line) or\
                 re.match(".*Helper.*", line) or\
                 re.match(".*~~>.*", line) or\
                 re.match(".*=.*=.*", line):
                    prioritize(goal, 95, line)
            elif re.match(".*KU\( 'g'\^\(~xx\*~yy\).*", line) or\
                 re.match(".*KU\( 'g'\^\(~yy\*~xx\).*", line):
                    prioritize(goal, 90, line)
            elif \
                 re.match(".*KU\( expa.*", line) or\
                 re.match(".*KU\( extr.*", line):
                    prioritize(goal, 80, line)
            elif re.match(".*LTKRev.*", line) or\
                 re.match(".*sign.*", line) or\
                 re.match(".*StI.*", line) or\
                 re.match(".*StR.*", line) or\
                 re.match(".*aead.*", line):
                    prioritize(goal, 70, line)
            elif re.match(".*KU\( h\(.*", line):
                    prioritize(goal, 60, line)
            elif re.match(".*KU\( \(.V⊕.*", line):
                    prioritize(goal, 40, line)
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



