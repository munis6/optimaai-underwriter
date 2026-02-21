from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.colors import HexColor

# -----------------------------
# Color Palette
# -----------------------------
PRIMARY_BLUE = colors.HexColor("#2A4B8D")
SECONDARY_BLUE = colors.HexColor("#6C87B5")
ACCENT_BG = colors.HexColor("#E8EEF7")
LIGHT_GRAY = colors.HexColor("#DDDDDD")
TEXT_DARK = colors.HexColor("#222222")

# -----------------------------
# Page Layout
# -----------------------------
PAGE_MARGIN_LEFT = 50
PAGE_MARGIN_RIGHT = 550

styles = getSampleStyleSheet()

# -----------------------------
# Typography Styles
# -----------------------------

# Page Title
TITLE_STYLE = ParagraphStyle(
    "TitleStyle",
    parent=styles["Heading1"],
    fontName="SourceSans3-Bold",
    fontSize=18,
    leading=22,
    textColor=TEXT_DARK,
    spaceAfter=14,
)

# Section Header
SECTION_HEADER_STYLE = ParagraphStyle(
    "SectionHeaderStyle",
    parent=styles["Heading2"],
    fontName="SourceSans3-Bold",
    fontSize=13,
    leading=16,
    textColor=PRIMARY_BLUE,
    spaceBefore=16,
    spaceAfter=8,
)

# Charcoal Accent Header (used on Page 1)
SECTION_HEADER_ACCENT = ParagraphStyle(
    "SectionHeaderAccent",
    parent=SECTION_HEADER_STYLE,
    textColor=HexColor("#333333"),
)

# Subheader (rarely used)
SUBHEADER_STYLE = ParagraphStyle(
    "SubheaderStyle",
    parent=styles["Heading3"],
    fontName="SourceSans3-Bold",
    fontSize=13,
    leading=16,
    textColor=TEXT_DARK,
    spaceBefore=10,
    spaceAfter=4,
)

# Body Text
BODY_STYLE = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontName="SourceSans3",
    fontSize=10,
    leading=14,
    textColor=TEXT_DARK,
)

# Micro Insight Text (used under risk score, premium, etc.)
MICRO_STYLE = ParagraphStyle(
    "MicroStyle",
    parent=styles["BodyText"],
    fontName="SourceSans3",
    fontSize=9,
    leading=12,
    textColor="#555555",
)

# Card Label (bold)
CARD_LABEL_STYLE = ParagraphStyle(
    "CardLabelStyle",
    parent=styles["BodyText"],
    fontName="SourceSans3-Bold",
    fontSize=10,
    leading=14,
    textColor=TEXT_DARK,
)

# Card Value (regular)
CARD_VALUE_STYLE = ParagraphStyle(
    "CardValueStyle",
    parent=styles["BodyText"],
    fontName="SourceSans3",
    fontSize=11,
    leading=14,
    textColor=TEXT_DARK,
)
