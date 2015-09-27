__author__ = 'Kor'

"""
This program will read from the Roastmaster database and output a menu of the
current roasts
"""

import sqlite3 as lite
import os
import shutil
from datetime import datetime, timedelta
# import tempfile
import subprocess

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import arrow


def create_report():
    """ These are the default style properties for the paragraph class:

    class ParagraphStyle(PropertySet):
        defaults = {
        'fontName':'Times-Roman',
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'Times-Roman',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        }"""

    styletitle1 = ParagraphStyle(
        name='Normal',
        leftIndent=14,
        fontName='Times-Bold',
        fontSize=18,
        textColor='Black')

    styletitle2 = ParagraphStyle(
        name='Normal',
        leftIndent=7,
        fontName='Times-Bold',
        fontSize=16,
        textColor='Black')

    styledata = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=14,
        textColor='Black')

    source_file_name = "d:/Development/RoastMaster/temp.txt"
    # pdf_file_name = tempfile.mktemp(".pdf")
    pdf_file_name = "coffee menu.pdf"
    stylesheet = getSampleStyleSheet()
    h1 = stylesheet["Heading1"]
    styleFS = stylesheet["Heading3"]
    normal = stylesheet["Normal"]
    # font12 = stylesheet['fontSize':12]
    width, height = letter

    doc = SimpleDocTemplate(pdf_file_name, pagesize=letter,
                            fontName='Times-Roman', fontSize=10)
    #
    # reportlab expects to see XML-compliant
    #  data; need to escape ampersands &c.
    #
    text = (open(source_file_name).read()).splitlines()

    #
    # Take the first line of the document as a
    #  header; the rest are treated as body text.
    #
    story = []
    story.append(Paragraph(text[0], styletitle1))
    story.append(Spacer(.5, 0.1 * inch))

    story.append(Paragraph(text[1], styletitle2))
    for line in text[2:]:
        story.append(Paragraph(line, styledata))
        story.append(Spacer(.5, 0.1 * inch))

    doc.build(story)
    # win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)
    subprocess.call(
        ['C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRD32.exe',
         pdf_file_name])


def get_choice():
    option_valid = False
    while not option_valid:
        try:
            choice = int(input("Option Selected: "))
            if 0 <= choice <= 2:
                option_valid = True
            else:
                print("Enter a valid option")
        except ValueError:
            print("Enter a valid option")
        return choice


def check_db(mydb):
    try:

        metadata = os.stat(mydb)
    except IOError:
        print("File does not exist. Correct the problem and restart.")

    oldDB = metadata.st_mtime
    metadata = os.stat('roast_master.db')
    newDB = metadata.st_mtime

    if oldDB > newDB:
        print(
            'There is a newer version of the database available, Would you '
            'like '
            'to replace the old database with the newer one?')
        print('0. Exit the program')
        print('1. No, keep the existing database.')
        print('2. Yes, replace the old database with the newer one.')

        choice = get_choice()

        if choice == 0:
            exit()
        elif choice == 1:
            return
        elif choice == 2:

            shutil.copyfile(
                'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite',
                'd:/development/roastmaster/roast_master.db')
        else:
            print("Keeping current database")


def get_date(time_now, dateFormat="%d-%m-%Y", addDays=0):
    time_now = datetime.now()
    # print("time_now: ", time_now)
    if (addDays != 0):
        anotherTime = time_now + timedelta(days=addDays)
    else:
        anotherTime = time_now

    return anotherTime.strftime(dateFormat)


def show_coffee_list():
    con = lite.connect('D:/development/roastmaster/roast_master.db')
    f = open('temp.txt', "w")

    with con:

        # row_factory = lite.Row
        cur = con.cursor()
        # SELECT datetime( r.ZDATE, 'unixepoch', '31 YEARS', '+1 day',
        # 'localtime' ) AS Date,

        sql = """  Select
                   r.ZDATE AS Date,
                   b.ZMARKETNAME AS [Market Name],
                   CASE
                        WHEN b.zgrade IS NOT NULL THEN b.zgrade
                        ELSE ''
                   END AS Grade,

                   ( CAST ( CAST ( r.ZDURATION / 60.0 AS int )  AS string )
                   || ':' || CAST ( ZDURATION % 60 AS string )  ) AS Duration
              FROM ((ZROAST r
                    JOIN ZROASTEDITEM i  ON i.ZROAST = r.Z_PK)

                       JOIN ZBEAN b
                         ON i.ZBEAN = b.Z_PK
                       JOIN zcountry c
                         ON b.zcountry = c.z_pk
            )

             WHERE ZDATE >=( strftime( '%s', '2015-08-01 00:00:00 -05:00' )
             - strftime( '%s', '2001-01-01 00:00:00' )  )
                   AND
                   r.zagtron = 1

             ORDER BY ZDATE DESC;
          """

        cur.execute(sql)
        report = []
        aline = "Tubby's Specialty Coffee"
        f.write(aline + '\n')
        aline = 'Menu for ' + arrow.now().format('dddd MMMM D')
        f.write(aline + '\n')
        print(aline)
        report.append(aline)

        col_names = [cn[0] for cn in cur.description]



        # print(
        #     "{0:<19} {1:21}{2:15}{3}".format(col_names[0],
        #                                      col_names[1], col_names[2],
        #                                      col_names[3]))

        print('_' * 60)
        aline = '_' * 40
        f.write(aline + '\n')
        report.append(aline)
        # for each in (cur.fetchall()):
        #     for col in each:
        #         if col == None:
        #             col = 'None'
        #
        #         print("{:32}".format(col), end='')
        #     print()
        for each in (cur.fetchall()):
            # temp = each[1]
            # temp = datetime.fromtimestamp(each[1] +
            # epoch_delta.total_seconds())
            temp = arrow.Arrow.fromtimestamp(each[0])

            date = temp.replace(years=31)
            date = date.format('MM/DD')
            # if debug:
            #     print("Date: ", type(date))
            #
            #     print("The Date: ", date)

            # temp2 = datetime.strptime("Tue Aug 25 16:02:44 2015", "%a %b %d
            #  %H:%M:%S %Y")
            # temp2 = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
            # temp3 = temp2.strftime("%a %b %d")
            # temp4 = temp2.strftime("%a %b %d")

            if debug:
                print(
                    "{0:26}  {1:26}{2:15}{3}".format(each[1], each[0], each[2],
                                                     each[3]))
            else:
                aline = (
                    "{0:19} {1:20} {2} -- {3}".format(each[1], each[2], '    ',
                                                      date))
                f.write(aline + '\n')
                report.append(aline)
                print(aline)
                # print(
                #     "{0:19} {1:10} {2}".format(date, each[1], each[2]))

        print('_' * 60)
        aline = ('_' * 40)
        report.append(aline)
        f.write(aline + '\n')
        f.close()
        f = open("temp.txt", "r")

        f.close()

        # create_report(report)


debug = False
roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
check_db(roastmaster_db)
show_coffee_list()
create_report()
