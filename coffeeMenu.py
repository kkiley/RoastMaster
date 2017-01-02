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
    print("In create_report")
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
        leftIndent=50, # 28
        fontName='Times-Bold',
        fontSize=20,
        textColor='Blue')

    styletitle2 = ParagraphStyle(
        name='Normal',
        leftIndent=1, # 46
        fontName='Times-Bold',
        fontSize=17,
        textColor='Green')

    styletitle3 = ParagraphStyle(
        name='Normal',
        leftIndent=14,
        fontName='Times-Bold',
        fontSize=18,
        textColor='Red')

    styletitle4 = ParagraphStyle(
        name='Normal',
        leftIndent=7,
        fontName='Times-Bold',
        fontSize=16,
        textColor='Green')

    styledata = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=14,
        textColor='Blue')

    styledata1 = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=14,
        textColor='Black')

    styledata2 = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=14,
        textColor='Red')

    source_file_name = "temp.txt"
    # source_file_name = "d:/Development/RoastMaster/temp.txt"
    # pdf_file_name = tempfile.mktemp(".pdf")
    pdf_file_name = "coffee menu.pdf"
    stylesheet = getSampleStyleSheet()
    # h1 = stylesheet["Heading1"]
    # styleFS = stylesheet["Heading3"]
    # normal = stylesheet["Normal"]
    # font12 = stylesheet['fontSize':12]
    # width, height = letter

    doc = SimpleDocTemplate(pdf_file_name, pagesize=letter,
                            fontName='Times-Roman', fontSize=10)
    #
    # reportlab expects to see XML-compliant
    #  data; need to escape ampersands &c.
    #
    text = (open(source_file_name).read()).splitlines()
    # for line in text:
    #     print(line)

    #
    # Take the first line of the document as a
    #  header; the rest are treated as body text.
    #
    # print("Hello")
    # print(text[0])
    story = [Paragraph(text[0], styletitle1), Spacer(.5, 0.1 * inch),  Paragraph(text[1], styletitle2),
             Paragraph(text[2], styledata1), Spacer(.5, 0.1 * inch)]
    # num = 0
    # for line in story:
    #     print(num, line)
    #     num += 1


    for line in text[3:]:
        story.append(Paragraph(line, styledata1))
        story.append(Spacer(.5, 0.1 * inch))

    doc.build(story)
    # win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)
    subprocess.call(
        # ['C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRD32.exe'
        # ['C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Acrobat Reader DC'
        ['C:\Program Files\Tracker Software\PDF Editor\PDFXEdit.exe'
        , pdf_file_name])


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
    metadata = os.stat('../roast_master.db')
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
                '../roast_master.db')
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


def show_coffee_list(debug):
    # con = lite.connect('D:/development/roastmaster/roast_master.db')
    # con = lite.connect('../roast_master.db')


    print("In show_coffee_list")
    con = lite.connect('../roast_master.db')
    # con = lite.connect('D:/development/roastmaster/roast_master.db')
    f = open('temp.txt', "w")
    time_span = -15

    unix_epoch = '2001-01-01 00:00:00'
    time_interval = arrow.now()
    time_interval = time_interval.replace(years=0, days=time_span, hours=-5)
    time_interval = time_interval.format('YYYY-MM-DD hh:mm:ss')

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()

        sql = """
    SELECT r.zdate AS [Roast Date],
           c.zname AS [Country of Origin],
           b.zmarketname AS [Market Name]
      FROM ZROAST r
           JOIN
           ZROASTEDITEM i ON i.ZROAST = r.Z_PK
           JOIN
           zbean b ON i.zbean = b.z_pk
           JOIN
           zcountry c ON b.zcountry = c.z_pk
           LEFT JOIN
           zdensity d ON b.zdensity = d.z_pk
    WHERE r.zdate >=( strftime( '%s', ? )  - strftime( '%s', ? )  )

    AND     r.ZAGTRON = 1
    ORDER BY r.zdate DESC;
           """
        previous_roast = ''
        roast = []
        oldtime = ''


        # sql = """  Select
        #            r.ZDATE AS Date,
        #            b.ZMARKETNAME AS [Market Name],
        #            CASE
        #                 WHEN b.zgrade IS NOT NULL THEN b.zgrade
        #                 ELSE ''
        #            END AS Grade,
        #
        #            ( CAST ( CAST ( r.ZDURATION / 60.0 AS int )  AS string )
        #            || ':' || CAST ( ZDURATION % 60 AS string )  ) AS Duration
        #       FROM ((ZROAST r
        #             JOIN ZROASTEDITEM i  ON i.ZROAST = r.Z_PK)
        #
        #                JOIN ZBEAN b
        #                  ON i.ZBEAN = b.Z_PK
        #                JOIN zcountry c
        #                  ON b.zcountry = c.z_pk
        #     )
        #
        #      WHERE ZDATE >=( strftime( '%s', '2015-08-01 00:00:00 -05:00' )
        #      - strftime( '%s', '2001-01-01 00:00:00' )  )
        #            AND
        #            r.zagtron = 1
        #
        #      ORDER BY ZDATE DESC;
        #   """

        # cur.execute(sql)
        cur.execute(sql, (time_interval, unix_epoch))

        # report = []
        aline = "Wuffy's Cafe"
        # aline = "Tubby's Specialty Coffee"
        f.write(aline + '\n')
        # aline =	'Menu for Christmas Day 2015'
        aline = 'Menu for ' + arrow.now().format('dddd MMMM D')
        f.write(aline + '\n')
        # print(aline)
        # report.append(aline)

        # print('_' * 60)
        aline = '_' * 47
        f.write(aline + '\n')
        # report.append(aline)
        col_names = [cn[0] for cn in cur.description]
        # for name in col_names:
        #     print(':' + name)

        for each in (cur.fetchall()):
            # UNIX epoch is 31 years and 1 day earlier than Code Data time
            # Format date():

            temp = arrow.Arrow.fromtimestamp(each["Roast Date"])

            # 10/24/16 I'm not sure about days=0 below. Sometimes days=1 works but
            # I changed to days=0 because the date was 1 day ahead
            date = temp.replace(years=31, days=0)
            date = date.format('MM/DD/YY hh:mm')

            pdate = temp.replace(years=31, days=0)
            pdate = pdate.format('MM/DD')

            # print(pdate)

            # if debug:
            #     print(
            #         "{0:26}  {1:26}{2:15}{3}".format(each["Country of Origin"], each["Roast Date"], each["Market Name"]))
            # else:
            aline = (
                " {1:20} {2} - {3}".format(each["Country of Origin"], each["Market Name"], '    ',
                                                  pdate))
            # print(aline)
            if date != oldtime:
                roast.append(previous_roast)
                previous_roast = aline
                oldtime = date

            previous_roast = aline

        roast.append(aline)

        for a_record in roast:
            f.write(a_record + '\n')
            # print(a_record)
            # report.append(aline)

            # f.write(aline + '\n')
            # report.append(aline)
            # print(aline)

        # print('_' * 60)
        # aline = ('_' * 47)
        # report.append(aline)
        # f.write(aline + '\n')
        f.close()
        f = open("temp.txt", "r")

        f.close()

        # create_report(report)

if __name__ == '__main__':

    debug = False
    roastmaster_db = 'C:/Users/kor/Dropbox/Apps/Roastmaster/Kor Database.sqlite'
    # roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
    check_db(roastmaster_db)
    show_coffee_list(debug)
    create_report()
