from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


#Common config options

fonts = {
    "GaramondRegular": "../../.fonts/13308.ttf",
    "GaramondBold": "../../.fonts/12735.ttf"
}

# Options to get dete from csv file

BADGE_TYPE_NONE = 0
BADGE_TYPE_XIX = 1
BADGE_TYPE_BAR = 2
BADGE_TYPE_XVI = 4
BADGE_TYPE_ORG = 0xFF
BADGE_TYPE_FULL = BADGE_TYPE_XIX | BADGE_TYPE_BAR | BADGE_TYPE_XVI

### This is actually required function to turn csv row into dictionary to be processed
def getDataFields(row):
    return {
        "NameR": row[0],
        "city": row[1],
        "type": getBadgeType(row[6], row[7])
    }

### Support dat and functions for common case

badgeTypeStrings = {
    BADGE_TYPE_XIX: "19",
    BADGE_TYPE_BAR: "бар",
    BADGE_TYPE_XVI: "16",
    BADGE_TYPE_ORG: "орг",
    BADGE_TYPE_FULL: "полный"
}

def getBadgeType(paid, what):
    paid.strip()
    if not paid:
        return BADGE_TYPE_NONE
    ret = BADGE_TYPE_NONE
    for t, s in badgeTypeStrings.items():
        if s in what:
            ret |= t
    return ret

### Badges layout

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
badgePageSize = (320 * mm, 450 * mm)
badgePrintBox = (9 * mm, 10 * mm, 311 * mm, 440 * mm)

badgeFieldsF = {
    "NameR": (canvas.Canvas.drawCentredString, 47 * mm, 45 * mm, 86 * mm,
              ("GaramondBold", 8 * mm)),
    "city": (canvas.Canvas.drawCentredString, 47 * mm, 33 * mm, 86 * mm,
             ("GaramondRegular", 6 * mm)),
}

badgeFieldsB = {}

### Certificates layout
CERT_FILE = "./CertFST18.png"
certImageFiles = {
    BADGE_TYPE_NONE: CERT_FILE,
    BADGE_TYPE_XIX: CERT_FILE,
    BADGE_TYPE_BAR: CERT_FILE,
    BADGE_TYPE_XIX | BADGE_TYPE_BAR: CERT_FILE,
    BADGE_TYPE_XIX | BADGE_TYPE_XVI: CERT_FILE,
    BADGE_TYPE_XVI: CERT_FILE,
    BADGE_TYPE_XVI | BADGE_TYPE_BAR: CERT_FILE,
    BADGE_TYPE_ORG: CERT_FILE,
    BADGE_TYPE_FULL: CERT_FILE,
}
certImageColors = {
    BADGE_TYPE_NONE: '#ffffff',
    BADGE_TYPE_XIX: '#ffffff',
    BADGE_TYPE_BAR: '#ffffff',
    BADGE_TYPE_XIX | BADGE_TYPE_BAR: '#ffffff',
    BADGE_TYPE_XIX | BADGE_TYPE_XVI: '#ffffff',
    BADGE_TYPE_XVI: '#ffffff',
    BADGE_TYPE_XVI | BADGE_TYPE_BAR: '#ffffff',
    BADGE_TYPE_ORG: '#ffffff',
    BADGE_TYPE_FULL: '#ffffff'
    }

certImageSize = (210 * mm, 297 * mm)
certPageSize = (210 * mm, 297 * mm)
certPrintBox = (0 * mm, 0 * mm, 210 * mm, 297 * mm)

certFields = {
    "NameR": (canvas.Canvas.drawCentredString, 105 * mm, 179 * mm, 150 * mm,
              ("GaramondBold", 10 * mm)),
}

### What to print
printTask = {
    'badges': {
        'splits': ('-fw','-bk'), # Two sided
        'page': {
            'size': badgePageSize,
            'box': badgePrintBox,
        },
        'images': {
            'size': badgeImageSize,
            'files': badgeImageFiles, # dict by types
            'colors': badgeImageColors, # dict by types
        },
        'fields': (badgeFieldsF , badgeFieldsB) # For two sides
    },
    'certificates': {
        'splits': ('',), # One sided
        'page': {
            'size': certPageSize,
            'box': certPrintBox,
        },
        'images': {
            'size': certImageSize,
            'files': certImageFiles, # dict by types
            'colors': certImageColors, # dict by types
        },
        'fields': (certFields,)
    },
}
