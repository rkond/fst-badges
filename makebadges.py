#!/usr/bin/python3

import sys
from pprint import pprint

from reportlab.pdfgen import canvas

from config import *  #pylint: disable=W0401

from utils import drawItem, nextItem, readData

data = readData(sys.argv[1])
pprint(data)

fpages = canvas.Canvas('badgesf.pdf', pagesize=pageSize)
bpages = canvas.Canvas('badgesb.pdf', pagesize=pageSize)
x = printBox[0]
y = printBox[1]

for r in data:
    drawItem(fpages, x, y, badgeFieldsF, r)
    drawItem(bpages, printBox[3] - badgeImageSize[0] - x, y, badgeFieldsB, r)
    x, y = nextItem(x, y, (fpages, bpages))

fpages.save()
bpages.save()
