#!/usr/bin/python3

import sys
import csv
import reportlab
import pprint 

BADGE_TYPE_NONE = 0
BADGE_TYPE_XIX  = 1
BADGE_TYPE_BAR  = 2
BADGE_TYPE_XVI  = 4
BADGE_TYPE_ORG  = 0xFF
BADGE_TYPE_FULL = BADGE_TYPE_XIX | BADGE_TYPE_BAR | BADGE_TYPE_XVI

badgeTypeStrings = {
    BADGE_TYPE_XIX      :"19",  
    BADGE_TYPE_BAR      :"бар",
    BADGE_TYPE_XVI      :"16",
    BADGE_TYPE_ORG      :"орг",
    BADGE_TYPE_FULL     :"полный"
}

def getBadgeType(paid,what):
    paid.strip()
    if not paid:
        return BADGE_TYPE_NONE
    ret = BADGE_TYPE_NONE
    for t,s in badgeTypeStrings.items():
        if s in what:
            ret |= t
    return ret

data = []
with open(sys.argv[1]) as csvfile:
    rd = csv.reader(csvfile)
    rd.__next__() # Skip fiirst row
    data = [ {
        "NameR":row[0],
        "city": row[1],
        "paid": getBadgeType(row[6],row[7])
         } for row in rd ] 

pprint.pprint(data)
