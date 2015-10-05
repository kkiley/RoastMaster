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
    time_span = -30
    unix_epoch = '2001-01-01 00:00:00'
    time_interval = arrow.now()
    time_interval = time_interval.replace(years=0, days=time_span, hours=-5)
    time_interval = time_interval.format('YYYY-MM-DD hh:mm:ss')

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()

        sql = """
        SELECT r.zdate AS Date,
               r.zduration AS [Roast Duration],
               cu.zname AS [Curve Type],
               n.ztime AS [Node Time],
               n.zlevel AS [Node Temp],
               e.zeventtitle AS Event,
               e.zeventtime AS [Time of Event],
               r.zfirstcrack AS [First Crack],
               rt.zmanufacturer AS [Roaster Make],
               i.zamount AS [Charge Weight],
               b.zcountry AS [Country Pointer],
               co.zname AS [Country]
          FROM zcurve cu
               JOIN zroast r
                 ON r.z_pk = cu.zroast
               JOIN zroasteditem i
                 ON r.z_pk = i.zroast
               JOIN znode n
                 ON n.zcurve = cu.z_pk
               JOIN zevent e
                 ON e.zcurve = cu.z_pk
               JOIN zbean b
                 ON b.z_pk = i.zbean
               JOIN zcountry co
                 ON b.zcountry = co.z_pk
               JOIN zroaster rt
                 ON rt.z_pk = r.zroaster
        WHERE r.zdate >=( strftime( '%s', ? )  - strftime( '%s', ? )  )
--         WHERE r.zdate >=( strftime( '%s', '2015-09-15 00:00:00 -05:00' )  - strftime( '%s', '2001-01-01 00:00:00' )  )
               AND
               e.zeventtime IS NOT NULL
               AND
               cu.zname IN ('BT', 'Bean Temperature')
               AND
               ( e.ztriggertype = 0
               OR
               e.ztriggertype = 2 )
--               AND e.zeventtitle IN ("Dry End", "Drying End")
        ORDER BY zdate DESC;
          """
        previous_roast = ''
        roast = []
        oldtime = ''
        # new_time = False
        begun = False

        cur.execute(sql, (time_interval, unix_epoch))

        aline = arrow.now().format('dddd MMMM D') + ' ' * 20 + "Data to paste in Roastmaster"
        f.write(aline + '\n\n')
        print(aline)

        col_names = [cn[0] for cn in cur.description]

        aline = "{0:<19} {1:15} {2:12} {3} {4} {5} {6}".format(col_names[0],
                                                               col_names[1], col_names[2],
                                                               col_names[3], col_names[4],
                                                               col_names[5], col_names[6],
                                                               col_names[7])
        # f.write(aline + '\n')

        print(
            "0: {0:<17} 1: {1:15} 2: {2:13} 3: {3:16} 4: {4:10} 5: {5:10} 6: {6:11} 7: {7:} 8: {8:}"
            "9: {9:}, 10: {10:} 11: {11:}".format(col_names[0],
                                                                           col_names[1],
                                                                           col_names[2],
                                                                           col_names[3],
                                                                           col_names[4],
                                                                           col_names[5],
                                                                           col_names[6],
                                                                           col_names[7],
                                        col_names[8], col_names[9], col_names[10], col_names[11]))

        print('_' * 140)
        aline = '_' * 40
        # f.write(aline + '\n')
        dry_time = 0.0
        dry_percent = 0.0

        for each in (cur.fetchall()):

            # date = each[0]
            # roast_duration = each[1]
            # curve_type = each[2]
            # node_time = each[3]
            # node_temp = each[4]
            # event = each[5]
            # event_time = each[6]
            # first_crack = each[7]
            # roaster_brand = each[8]
            # bean_amount = each[9]
            # country_code = each[10]
            # country = each[11]


            # UNIX epoch is 31 years and 1 day earlier than Code Data time
            # Format date():
            temp = arrow.Arrow.fromtimestamp(each["Date"])
            date = temp.replace(years=31, days=1)
            date = date.format('YYYY-MM-DD hh:mm')

            if not begun:
                oldtime = date
                begun = True

            # turnaround_time = time.strftime("%M:%S", time.gmtime(each[3]))
            roast_duration = time.strftime("%M:%S", time.gmtime(each[1]))
            event_time = time.strftime("%M:%S", time.gmtime(each[7]))
            if each["Event"] == 'Drying End' or each["Event"] == 'Dry End':
                dry_time = each["Time of Event"]
                print('dry_time: ' + str(each["Time of Event"]))
            elif each["Event"] == 'Turnaround':
                turn_temp = each[7]
                turn_temp = format_time(turn_temp)
            else:
                print('Invalid Event Type '  + str(each["Event"]))
                # exit()
            dry_percent = get_phase_percent(0, dry_time, each["Roast Duration"])
            drying_stage = dry_time
            # dry_percent = '{:.1%}'.format(dry_time/each[1])
            # dry_percent = str(dry_percent) + '%'
            drying_stage = time.strftime("%M:%S", time.gmtime(drying_stage))
            ramp_stage = each["First Crack"] - dry_time
            ramp_stage = time.strftime("%M:%S", time.gmtime(ramp_stage))
            ramp_percent = get_phase_percent(dry_time, each["First Crack"], each["Roast Duration"])
            development = each["Roast Duration"] - each["First Crack"]
            development = time.strftime("%M:%S", time.gmtime(development))
            development_percent = get_phase_percent(each["First Crack"], each["Roast Duration"], each["Roast Duration"])
            # What Woofie wants
            # Charge, duration, dry time & %, ramp time & %, Development time & %, Roaster,
            # amount, bean
            # 420f,   13:05,    4:47-40%      3:45-31%       3:31-29,              Huky,
            # 350g,   Kenya
            # aline = (
            #     "{0:<17} {1:15} {2:13} {3:16} {4:<10} {5:<10} {6:11} {7} {8} {9}".format(date,
            #  roast_duration, each[2],
            #     each[3], int(each[4]), int(each[5]), each[6], event_time, turn_temp,
            # dry_percent))

            aline = (
                "{0:}f, {1:}, {2:}-{3:} {4:}-{5:} {6:}-{7:}, {8:}, {9:}g, {10:}  ----{11:}".format(
                    int(each["Node Temp"]), roast_duration,
                    drying_stage, dry_percent, ramp_stage, ramp_percent, development,
                    development_percent, each["Roaster Make"], each["Charge Weight"], each["Country"], date))
            if date != oldtime:
                roast.append(previous_roast)
                previous_roast = aline
                oldtime = date

            previous_roast = aline

            # f.write(aline + '\n')
            print(aline)
        roast.append(aline)

        # print('Debug info:')
        # print('-' * 50)
        for a_record in roast:
            f.write(a_record + '\n')

        print('_' * 60)

        aline = ('_' * 40)
        # f.write(aline + '\n')
        f.close()
        f = open("temp.txt", "r")

        f.close()


debug = False
roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
check_db(roastmaster_db)
show_coffee_list()
create_report()
