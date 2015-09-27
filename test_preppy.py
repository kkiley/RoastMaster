import datetime
import csv
import sys

from z3c.rml import rml2pdf
import preppy


def fetchTable():
    # Initialize the result array ...
    data = []

    # ... and parse the content.
    with open('data.csv', 'r') as csvFile:
        for row in csv.reader(csvFile, delimiter=','):
            rowData = []

            for key, col in enumerate(row):
                rowData.append(col)

            data.append(rowData)

    return data


def main(argv):
    # Load the rml template into the preprocessor, ...
    template = preppy.getModule('testDoc.prep')

    # ... fetch the table data ...
    table = fetchTable()

    # ... and do the preprocessing.
    rmlText = template.get(
        datetime.datetime.now().strftime("%Y-%m-%d"), 'Andreas Wilhelm',
        'www.avedo.net', 'info@avedo.net', table)

    # Finally generate the *.pdf output ...
    pdf = rml2pdf.parseString(rmlText)

    # ... and save it.
    with open('rmlReport.pdf', 'w') as pdfFile:
        pdfFile.write(pdf.read())


if __name__ == '__main__':
    main(sys.argv[1:])
