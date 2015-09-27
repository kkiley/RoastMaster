__author__ = 'Kor'

"""
This program will read from the Roastmaster database and output a menu of the
current roasts
"""

# todo Create function to print output to a pdf
# Todo Create function to print a temp pdf file

import sqlite3 as lite
import os
import shutil
from datetime import datetime, timedelta
import tempfile
import subprocess
import time

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import arrow


# import preppy
# import trml2pdf
# import rlextra
# from rlextra import rml2pdf

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
        fontSize=12,
        textColor='Black')

    source_file_name = "d:/Development/RoastMaster/temp.txt"
    pdf_file_name = tempfile.mktemp(".pdf")
    # pdf_file_name = "kor coffee menuf"
    # stylesheet = getSampleStyleSheet()
    # h1 = stylesheet["Heading1"]
    # styleFS = stylesheet["Heading3"]
    # normal = stylesheet["Normal"]
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
    story.append(Spacer(.5, 0.1 * inch))

    for line in text[2:]:
        story.append(Paragraph(line, styledata))
        story.append(Spacer(.5, 0.1 * inch))

    doc.build(story)
    # win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)
    # subprocess.call(
    #     ['C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRD32.exe',
    #      pdf_file_name])
    subprocess.call(['write.exe', source_file_name])


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


def get_phase_percent(begin_time, end_time, roast_duration):
    stage_duration = end_time - begin_time
    return '{:.1%}'.format(stage_duration / roast_duration)


def format_time(target_time):
    return time.strftime("%M:%S", time.gmtime(target_time))


def show_coffee_list():
    con = lite.connect('D:/development/roastmaster/roast_master.db')
    f = open('temp.txt', "w")

    with con:
        # row_factory = lite.Row
        cur = con.cursor()
        # SELECT datetime( r.ZDATE, 'unixepoch', '31 YEARS', '+1 day',
        # 'localtime' ) AS Date,

        sql = """  SELECT r.zdate AS Date,
       r.zduration as [Roast Duration],
       rd.zname as [Roast Degree],
       cu.zname as [Curve Type],
       n.ztime as [Node Time],
       n.zlevel as [Node Temp],
       e.zeventtitle AS Event,
       e.zeventtime AS [Time of Event]
  FROM ( ( ( zcurve cu
       JOIN znode n
         ON n.zcurve = cu.z_pk )
       JOIN zevent e
         ON e.zcurve = cu.z_pk )
       JOIN zroast r
         ON r.z_pk = cu.zroast )
       JOIN zroastdegree rd
         ON rd.z_pk = r.zdegree
 WHERE r.zdate >=( strftime( '%s', '2015-09-15 00:00:00 -05:00' )  - strftime( '%s', '2001-01-01
 00:00:00' )  )
       AND
       upper( cu.zname ) = 'BEAN TEMPERATURE'
       AND
       ( e.ztriggertype = 0
       OR
       e.ztriggertype = 2 )
 ORDER BY zdate;

          """
        previous_roast = ''
        roast = []
        oldtime = ''
        new_time = False
        begun = False

        cur.execute(sql)
        report = []
        aline = arrow.now().format('dddd MMMM D') + ' ' * 20 + "Data to paste in Roastmaster"
        f.write(aline + '\n\n')
        print(aline)
        report.append(aline)

        col_names = [cn[0] for cn in cur.description]

        aline = "{0:<19} {1:15} {2:12} {3} {4} {5} {6}".format(col_names[0],
                                                               col_names[1], col_names[2],
                                                               col_names[3], col_names[4],
                                                               col_names[5], col_names[6],
                                                               col_names[7])
        # f.write(aline + '\n')

        print(
            "{0:<17} {1:15} {2:13} {3:16} {4:10} {5:10} {6:11} {7}".format(col_names[0],
                                                                           col_names[1],
                                                                           col_names[2],
                                                                           col_names[3],
                                                                           col_names[4],
                                                                           col_names[5],
                                                                           col_names[6],
                                                                           col_names[7]))

        print('_' * 140)
        aline = '_' * 40
        # f.write(aline + '\n')
        report.append(aline)
        dry_temp = 0.0
        dry_percent = 0.0

        for each in (cur.fetchall()):

            temp = arrow.Arrow.fromtimestamp(each[0])
            # UNIX epoch is 31 years and 1 day earlier than Code Data time
            date = temp.replace(years=31, days=1)
            date = date.format('YYYY-MM-DD HH:MM')

            if not begun:
                oldtime = date
                begun = True

            # turnaround_time = time.strftime("%M:%S", time.gmtime(each[3]))
            roast_duration = time.strftime("%M:%S", time.gmtime(each[1]))
            event_time = time.strftime("%M:%S", time.gmtime(each[7]))
            if each[6] == 'Drying End':
                dry_temp = each[7]
                # print('Dry: ' + str(each[7]))
            elif each[6] == 'Turnaround':
                turn_temp = each[7]
                turn_temp = format_time(turn_temp)
            else:
                print('Invalid Event Type')
                exit()
            dry_percent = get_phase_percent(0, dry_temp, each[1])
            drying_stage = dry_temp
            # dry_percent = '{:.1%}'.format(dry_temp/each[1])
            # dry_percent = str(dry_percent) + '%'
            drying_stage = time.strftime("%M:%S", time.gmtime(drying_stage))

            if debug:
                print(
                    "{0:26}  {1:26}{2:15}{3}{4}".format(each[1], each[0], each[2], each[3],
                                                        each[4]))
            else:
                aline = (
                    "{0:<17} {1:15} {2:13} {3:16} {4:<10} {5:<10} {6:11} {7} {8} {9}".format(date,
                                                                                             roast_duration,
                                                                                             each[
                                                                                                 2],
                                                                                             each[
                                                                                                 3],
                                                                                             int(
                                                                                                 each[
                                                                                                     4]),
                                                                                             int(
                                                                                                 each[
                                                                                                     5]),
                                                                                             each[
                                                                                                 6],
                                                                                             event_time,
                                                                                             turn_temp,
                                                                                             dry_percent))
                if date != oldtime:
                    roast.append(previous_roast)
                    previous_roast = aline
                    oldtime = date

                previous_roast = aline

                # f.write(aline + '\n')
                report.append(aline)
                print(aline)
        roast.append(aline)

        print('Debug info:')
        print('-' * 50)
        for a_record in roast:
            f.write(a_record + '\n')

        print('_' * 60)

        aline = ('_' * 40)
        report.append(aline)
        # f.write(aline + '\n')
        f.close()
        f = open("temp.txt", "r")

        f.close()

        # create_report(report)


debug = False
roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
check_db(roastmaster_db)
show_coffee_list()
create_report()
