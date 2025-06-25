import io
import csv

from pypdf import PdfReader, PdfWriter, PageObject

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor


pdfmetrics.registerFont(TTFont('Quicksand', 'fonts/Quicksand-Bold.ttf')) # set up nice font


# CONSTANTS
COLOURS = {'blue': HexColor('#0cc0df'), # blue represents sensors
           'green': HexColor('#00bf63'), # green represents electronics
           'yellow': HexColor('#ffbd59'), # yellow represents structural components
           'red': HexColor('#ff3131')} # red represents mechanical components
PAGE_WIDTH, PAGE_HEIGHT = A4
ROWS = 13
COLS = 5
MARGIN_X = 10
MARGIN_Y = 30
Y_PADDING = 10 # shift position within each sticker down by Y_PADDING
STICKER_WIDTH = (PAGE_WIDTH - 2 * MARGIN_X) / COLS
STICKER_HEIGHT = (PAGE_HEIGHT - 2 * MARGIN_Y) / ROWS
FONT_SIZE = 22
TEMPLATE_LOCATION = "templates/sticker-template.pdf"
STICKER_CSV = "stickers.csv"
OUTPUT_FILENAME = "stickers-output.pdf"
FONT = "Quicksand"



# Load sticker data
with open(STICKER_CSV, newline="") as f:
    stickers = list(csv.DictReader(f))

# Load template and prepare output
template_pdf = PdfReader(TEMPLATE_LOCATION)
output = PdfWriter()
base_page = template_pdf.pages[0]

# Paginate stickers
for i in range(0, len(stickers), ROWS * COLS):
    subset = stickers[i:i + ROWS * COLS]
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    for idx, sticker in enumerate(subset):
        row = idx // COLS
        col = idx % COLS

        x = MARGIN_X + col * STICKER_WIDTH + STICKER_WIDTH / 2
        y = PAGE_HEIGHT - MARGIN_Y - row * STICKER_HEIGHT - STICKER_HEIGHT / 2 - Y_PADDING

        c.setFont(FONT, FONT_SIZE)
        c.setFillColor(COLOURS[sticker['colour']])
        c.drawCentredString(x, y, sticker['text'])

    c.save()
    packet.seek(0)

    # Merge overlay with template
    overlay = PdfReader(packet).pages[0]
    merged = PageObject.create_blank_page(width=base_page.mediabox.width, height=base_page.mediabox.height)
    merged.merge_page(base_page)
    merged.merge_page(overlay)
    output.add_page(merged)

# Save final PDF
with open(OUTPUT_FILENAME, "wb") as f:
    output.write(f)
