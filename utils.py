from io import BytesIO

from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image, ImageColor
import csv

from config import fonts, getDataFields, mm, printTask

for faceName, fontFile in fonts.items():
    pdfmetrics.registerFont(TTFont(faceName, fontFile))


def makeImageReaderFromPIL(image):
    data = BytesIO()
    image.save(data, format='png')
    data.seek(0)
    return ImageReader(data)


def prepareImageSides(img, color, split=False):
    n = Image.new(mode='RGBA', size=img.size, color=ImageColor.getrgb(color))
    n.paste(img, mask=img)
    if split:
        w, h = n.size
        w //= 2
        return (makeImageReaderFromPIL(n.crop((0, 0, w, h))),
                makeImageReaderFromPIL(n.crop((w, 0, w * 2, h))))
    return (makeImageReaderFromPIL(n),)


def readData(filename):
    data = []
    with open(filename) as csvfile:
        rd = csv.reader(csvfile)
        rd.__next__()  # Skip the first row
        data = [getDataFields(row) for row in rd]
    return data


def drawItem(cnv, image_params, x, y, fields, row, side = 0):
    t = row["type"]
    cnv.drawImage(image_params['images'][t][side], x, y,
                  image_params['size'][0], image_params['size'][1])
    for n, f in fields.items():
        value = row[n]
        method, fx, fy, maxWidth, font = f
        fontFace, fontSize = font
        while pdfmetrics.stringWidth(value, fontFace, fontSize) > maxWidth:
            fontSize -= mm
        cnv.setFont(fontFace, fontSize)
        method(cnv, x + fx, y + fy, value)


def nextItem(image_params, page_params, x, y, canvases):
    x += image_params['size'][0]
    if x + image_params['size'][0] >= page_params['box'][2]:
        y += image_params['size'][1]
        x = page_params['box'][0]
    if y + image_params['size'][1] >= page_params['box'][3]:
        for c in canvases:
            c.showPage()
        y = page_params['box'][1]
    return x, y


for name, task in printTask.items():
    i = task['images']
    do_split = len(task['splits']) > 1
    i['images'] = {
        btype: prepareImageSides(
            Image.open(img), i['colors'][btype], do_split)
        for btype, img in task['images']['files'].items()
    }
