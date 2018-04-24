#!/usr/bin/python3

import sys
from pprint import pprint

from reportlab.pdfgen import canvas

from config import printTask  #pylint: disable=W0401

from utils import drawItem, nextItem, readData

data = readData(sys.argv[1])
pprint(data)

for name, task in printTask.items():
    do_split = bool(task['splits'])
    if do_split:
        pages = [canvas.Canvas(name+s+'.pdf', pagesize=task['page']['size']) for s in task['splits']]
    else:
        pages = [canvas.Canvas(name+'.pdf', pagesize=task['page']['size'])]

    x = task['page']['box'][0]
    y = task['page']['box'][1]

    for r in data:
        for i in range(len(task['splits'])):
            drawItem(pages[i], task['images'], task['page']['box'][2] - task['images']['size'][0] - x if i%2 else x , y, task['fields'][i], r, i)
        x, y = nextItem(task['images'], task['page'], x, y, pages)

    for c in pages:
        c.save()
