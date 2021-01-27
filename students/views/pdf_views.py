import io

from reportlab.pdfgen import canvas

from django.http import FileResponse



def test_pdf(request):
    # create file like buffer to recieve PDF data
    buffer = io.BytesIO()
    # create pdf using buffer file as pdf
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return FileResponse(buffer, filename='test_pdf.pdf')
