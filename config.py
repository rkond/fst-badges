from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

#Common config options

fonts = {
    "GaramondRegular": "../../.fonts/13308.ttf",
    "GaramondBold": "../../.fonts/12735.ttf",
    "LinoScript": "./LinoScript.ttf",
}

# Options to get dete from csv file

BADGE_TYPE_NONE = 0
BADGE_TYPE_GREEN = 1
BADGE_TYPE_GREY = 2
BADGE_TYPE_MAGENTA = 4
BADGE_TYPE_BLUE = 8
BADGE_TYPE_RED = 16
BADGE_TYPE_ORANGE = 32
BADGE_TYPE_YELLOW = 64
BADGE_TYPE_ORG = 0xFF


### This is actually required function to turn csv row into dictionary to be processed
def getDataFields(row):
    return {
        "NameR": row[0],
        "FNameE": row[5],
        "LNameE": row[4],
        "city": row[6],
        "level19": row[7],
        "levelBar": row[8],
        "type": getBadgeType(row[10])
    }


### Support dat and functions for common case

badgeTypeStrings = {
    BADGE_TYPE_GREEN: "зеленый",
    BADGE_TYPE_GREY: "серый",
    BADGE_TYPE_MAGENTA: "фиолетовый",
    BADGE_TYPE_BLUE: "синий",
    BADGE_TYPE_RED: "красный",
    BADGE_TYPE_ORANGE: "оранжевый",
    BADGE_TYPE_YELLOW: "желтый",
    BADGE_TYPE_ORG: "орг",
}


def getBadgeType(what):
    ret = BADGE_TYPE_NONE
    for t, s in badgeTypeStrings.items():
        if s in what:
            ret |= t
    return ret


### Badges layout

IMG_PATH_TEMPLATE = "./fst-badge-%s.png"
badgeImageFiles = {
    BADGE_TYPE_GREEN: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_GREY: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_MAGENTA: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_BLUE: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_RED: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_ORANGE: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_YELLOW: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_ORG: IMG_PATH_TEMPLATE % "no",
    BADGE_TYPE_NONE: IMG_PATH_TEMPLATE % "no",
}
badgeImageColors = {
    BADGE_TYPE_GREEN: "#60983d",
    BADGE_TYPE_GREY: "#bfbfbf",
    BADGE_TYPE_MAGENTA: "#bf6dbe",
    BADGE_TYPE_BLUE: "#6269bf",
    BADGE_TYPE_RED: "#bf6262",
    BADGE_TYPE_ORANGE: "#bf8d60",
    BADGE_TYPE_YELLOW: "#e0d771",
    BADGE_TYPE_ORG: "#71e0d9",
    BADGE_TYPE_NONE: "#ffffff"
}

badgeImageSize = (94 * mm, 59 * mm)
badgePageSize = (320 * mm, 450 * mm)
badgePrintBox = (9 * mm, 10 * mm, 311 * mm, 440 * mm)
#badgePageSize = (450 * mm, 320 * mm)
#badgePrintBox = (10 * mm, 9 * mm, 430 * mm, 302 * mm)

badgeFieldsB = {
    "FNameE": (canvas.Canvas.drawCentredString, 47 * mm, 38 * mm, 86 * mm,
               ("GaramondBold", 17 * mm)),
    "LNameE": (canvas.Canvas.drawCentredString, 47 * mm, 27 * mm, 86 * mm,
               ("GaramondBold", 8 * mm)),
    "city": (canvas.Canvas.drawCentredString, 47 * mm, 17 * mm, 40 * mm,
             ("GaramondRegular", 8 * mm)),
    "level19": (canvas.Canvas.drawCentredString, 17 * mm, 7 * mm, 16 * mm,
                ("GaramondRegular", 26 * mm)),
    "levelBar": (canvas.Canvas.drawCentredString, 77 * mm, 7 * mm, 16 * mm,
                 ("GaramondRegular", 26 * mm)),
}

badgeFieldsF = {}

### Certificates layout
CERT_FILE = "./CertFST18.png"
certImageFiles = {
    BADGE_TYPE_GREEN: CERT_FILE,
    BADGE_TYPE_GREY: CERT_FILE,
    BADGE_TYPE_MAGENTA: CERT_FILE,
    BADGE_TYPE_BLUE: CERT_FILE,
    BADGE_TYPE_RED: CERT_FILE,
    BADGE_TYPE_ORANGE: CERT_FILE,
    BADGE_TYPE_YELLOW: CERT_FILE,
    BADGE_TYPE_ORG: CERT_FILE,
    BADGE_TYPE_NONE: CERT_FILE,
}
certImageColors = {
    BADGE_TYPE_GREEN: "#ffffff",
    BADGE_TYPE_GREY: "#ffffff",
    BADGE_TYPE_MAGENTA: "#ffffff",
    BADGE_TYPE_BLUE: "#ffffff",
    BADGE_TYPE_RED: "#ffffff",
    BADGE_TYPE_ORANGE: "#ffffff",
    BADGE_TYPE_YELLOW: "#ffffff",
    BADGE_TYPE_ORG: "#ffffff",
    BADGE_TYPE_NONE: "#ffffff"
}

certImageSize = (210 * mm, 297 * mm)
#certPageSize = (210 * mm, 297 * mm)
#certPrintBox = (0 * mm, 0 * mm, 210 * mm, 297 * mm)
certPageSize = (450 * mm, 320 * mm)
certPrintBox = (10 * mm, 9 * mm, 440 * mm, 311 * mm)

certFields = {
    "NameR": (canvas.Canvas.drawCentredString, 105 * mm, 179 * mm, 170 * mm,
              ("LinoScript", 14 * mm)),
}

### What to print
printTask = {
    'badges': {
        'splits': ('-fw', '-bk'),  # Two sided
        'page': {
            'size': badgePageSize,
            'box': badgePrintBox,
        },
        'images': {
            'size': badgeImageSize,
            'files': badgeImageFiles,  # dict by types
            'colors': badgeImageColors,  # dict by types
        },
        'fields': (badgeFieldsF, badgeFieldsB)  # For two sides
    },
    'certificates': {
        'splits': ('', ),  # One sided
        'page': {
            'size': certPageSize,
            'box': certPrintBox,
        },
        'images': {
            'size': certImageSize,
            'files': certImageFiles,  # dict by types
            'colors': certImageColors,  # dict by types
        },
        'fields': (certFields, )
    },
}
