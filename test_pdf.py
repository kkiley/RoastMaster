__author__ = 'Kor'

# todo test reportlab pdf features to use in my Roastmaster reporting tool
# C:\ProgramData\Microsoft\Windows\Start Menu\Programs

import subprocess
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas




pdf_file = "D:/Development/RoastMaster/form.pdf"


def print_pdf(filename):
    subprocess.call(
        ['C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRD32.exe',
         pdf_file])


def create_report():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    width, height = letter

    canvas = canvas.Canvas("form.pdf", pagesize=letter)

    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    canvas.drawString(500, 750, "12/12/2010")
    canvas.line(480, 747, 580, 747)

    canvas.drawString(275, 725, 'AMOUNT OWED:')
    canvas.drawString(500, 725, "$1,000.00")
    canvas.line(378, 723, 580, 723)

    canvas.drawString(30, 703, 'RECEIVED BY:')
    canvas.line(110, 700, 580, 700)
    canvas.drawString(110, 703, "JOHN DOE")

    canvas.save()
    # c = canvas.Canvas(pdf_file, pagesize=letter)
    # c.drawString(100,750,"This is a test of reportlab")
    # c.save()


create_report()
print_pdf(pdf_file)
