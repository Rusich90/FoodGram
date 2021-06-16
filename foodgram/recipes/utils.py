from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from django.conf import settings
import io
from django.http import FileResponse


def create_pdf(purchases_dict):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    reportlab.rl_config.TTFSearchPath.append(
        str(settings.BASE_DIR) + '/fonts')
    pdfmetrics.registerFont(TTFont('FreeSans', '../fonts/FreeSans.ttf'))
    p.setFont('FreeSans', 20)
    p.drawString(250, 800, "FoodGram")
    p.drawString(30, 750, "Список покупок:")
    p.setFont('FreeSans', 16)
    x = 710
    for key, value in purchases_dict.items():
        p.drawString(30, x, f" - {key} - {value[0]} {value[1]}")
        x -= 30
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Список покупок.pdf')
