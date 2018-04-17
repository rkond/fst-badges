from io import BytesIO

from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image
import csv

from config import fonts, BADGE_TYPE_NONE, badgeTypeStrings, badgeImageFiles, badgeImageSize, printBox, getDataFields, mm

for faceName, fontFile in fonts.items():
    pdfmetrics.registerFont(TTFont(faceName, fontFile))


def splitImageSides(img):
    w, h = img.size
    w //= 2
    dataF = BytesIO()
    dataB = BytesIO()
    img.crop((0, 0, w, h)).save(dataF, format='png')
    img.crop((w, 0, w * 2, h)).save(dataB, format='png')
    dataF.seek(0)
    dataB.seek(0)
    return (ImageReader(dataF), ImageReader(dataB))


def readData(filename):
    data = []
    with open(filename) as csvfile:
        rd = csv.reader(csvfile)
        rd.__next__()  # Skip the first row
        data = [getDataFields(row) for row in rd]
    return data


def drawItem(cnv, x, y, fields, row):
    t = row["type"]
    cnv.drawImage(badgeImages[t][0], x, y, badgeImageSize[0],
                  badgeImageSize[1])
    for n, f in fields.items():
        value = row[n]
        method, fx, fy, maxWidth, font = f
        fontFace, fontSize = font
        while pdfmetrics.stringWidth(value, fontFace, fontSize) > maxWidth:
            fontSize -= mm
        cnv.setFont(fontFace, fontSize)
        method(cnv, x + fx, y + fy, value)


def nextItem(x, y, canvases):
    x += badgeImageSize[0]
    if x + badgeImageSize[0] + printBox[0] >= printBox[2]:
        y += badgeImageSize[1]
        x = printBox[0]
    if y + badgeImageSize[1] + printBox[1] >= printBox[3]:
        for c in canvases:
            c.showPage()
        y = printBox[1]
    return x, y


badgeImages = {
    t: splitImageSides(Image.open(img))
    for t, img in badgeImageFiles.items()
}
