from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

BADGE_TYPE_NONE = 0
BADGE_TYPE_XIX = 1
BADGE_TYPE_BAR = 2
BADGE_TYPE_XVI = 4
BADGE_TYPE_ORG = 0xFF
BADGE_TYPE_FULL = BADGE_TYPE_XIX | BADGE_TYPE_BAR | BADGE_TYPE_XVI

badgeTypeStrings = {
    BADGE_TYPE_XIX: "19",
    BADGE_TYPE_BAR: "бар",
    BADGE_TYPE_XVI: "16",
    BADGE_TYPE_ORG: "орг",
    BADGE_TYPE_FULL: "полный"
}
IMG_PATH_TEMPLATE = "./fst-badge-%s.png"
badgeImageFiles = {
    BADGE_TYPE_NONE: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_XIX: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_BAR: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_XIX | BADGE_TYPE_BAR: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_XIX | BADGE_TYPE_XVI: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_XVI: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_XVI | BADGE_TYPE_BAR: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_ORG: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_FULL: IMG_PATH_TEMPLATE % "no",
}
badgeImageColors = {
    BADGE_TYPE_NONE: '#888888',
    BADGE_TYPE_XIX: '#ff8888',
    BADGE_TYPE_BAR: '#88ff88',
    BADGE_TYPE_XIX | BADGE_TYPE_BAR: '#ffff88',
    BADGE_TYPE_XIX | BADGE_TYPE_XVI: '#ff88ff',
    BADGE_TYPE_XVI: '#8888ff',
    BADGE_TYPE_XVI | BADGE_TYPE_BAR: '#88ffff',
    BADGE_TYPE_ORG: '#ddeeff',
    BADGE_TYPE_FULL: '#ffffff'
    }

badgeImageSize = (94 * mm, 59 * mm)
pageSize = (320 * mm, 450 * mm)
printBox = (9 * mm, 10 * mm, 311 * mm, 440 * mm)

fonts = {
    "GaramondRegular": "../../.fonts/13308.ttf",
    "GaramondBold": "../../.fonts/12735.ttf"
}

badgeFieldsF = {
    "NameR": (canvas.Canvas.drawCentredString, 47 * mm, 45 * mm, 86 * mm,
              ("GaramondBold", 8 * mm)),
    "city": (canvas.Canvas.drawCentredString, 47 * mm, 33 * mm, 86 * mm,
             ("GaramondRegular", 6 * mm)),
}

badgeFieldsB = {}

## Functions to import the data from csv
def getBadgeType(paid, what):
    paid.strip()
    if not paid:
        return BADGE_TYPE_NONE
    ret = BADGE_TYPE_NONE
    for t, s in badgeTypeStrings.items():
        if s in what:
            ret |= t
    return ret

def getDataFields(row):
    return {
        "NameR": row[0],
        "city": row[1],
        "type": getBadgeType(row[6], row[7])
    }
