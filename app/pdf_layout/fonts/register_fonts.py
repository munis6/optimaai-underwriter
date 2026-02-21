from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

FONT_DIR = os.path.join(os.path.dirname(__file__))

def register_fonts():
    pdfmetrics.registerFont(TTFont("SourceSans3", os.path.join(FONT_DIR, "SourceSans3-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("SourceSans3-Bold", os.path.join(FONT_DIR, "SourceSans3-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("SourceSans3-SemiBold", os.path.join(FONT_DIR, "SourceSans3-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("SourceSans3-Italic", os.path.join(FONT_DIR, "SourceSans3-Italic.ttf")))
