__author__ = 'Kor'

"""
This program will read from the Roastmaster database and output data to a text file for
Pusstoe to paste into roastmaster
"""

import sqlite3 as lite
import os
import shutil
import subprocess
import time

import arrow

def create_report():

    # source_file_name = "temp.txt"
    source_file_name = "d:/Development/RoastMaster/temp.txt"
    text = (open(source_file_name).read()).splitlines()

    story = []
    story.append(text[0])

    story.append(text[1])

    for line in text[2:]:
        story.append(line)

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
        metadata = os.stat(mydb) #check My Database.sqlite on dropbox
    except IOError:
        print("File does not exist. Correct the problem and restart.")

    oldDB = metadata.st_mtime #get file date for dropbox file
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
            # Woofie's dropbox is here: C:\Users\kiley_000\Dropbox\Apps\Roastmaster
	    # Kor's dropbox is here: 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite',
            shutil.copyfile(
                'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite',
                'd:/development/roastmaster/roast_master.db')
        else:
            print("Keeping current database")


def get_phase_percent(begin_time, end_time, roast_duration):
    stage_duration = end_time - begin_time
    return '{:.1%}'.format(stage_duration / roast_duration)


def format_time(target_time):
    return time.strftime("%M:%S", time.gmtime(target_time))


def show_coffee_list():
    con = lite.connect('D:/development/roastmaster/roast_master.db')
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
        begun = False

        cur.execute(sql, (time_interval, unix_epoch))

        aline = arrow.now().format('dddd MMMM D') + ' ' * 20 + "Data to paste in Roastmaster"
        f.write(aline + '\n\n')

        col_names = [cn[0] for cn in cur.description]

        aline = "{0:<19} {1:15} {2:12} {3} {4} {5} {6}".format(col_names[0],
                                                               col_names[1], col_names[2],
                                                               col_names[3], col_names[4],
                                                               col_names[5], col_names[6],
                                                               col_names[7])


        dry_time = 0.0
        dry_percent = 0.0

        for each in (cur.fetchall()):

            # UNIX epoch is 31 years and 1 day earlier than Code Data time
            # Format date():
            temp = arrow.Arrow.fromtimestamp(each["Date"])
            date = temp.replace(years=31, days=1)
            date = date.format('YYYY-MM-DD hh:mm')

            if not begun:
                oldtime = date
                begun = True

            roast_duration = time.strftime("%M:%S", time.gmtime(each["Roast Duration"]))
            if each["Event"] == 'Drying End' or each["Event"] == 'Dry End':
                dry_time = each["Time of Event"]
            elif each["Event"] == 'Turnaround':
                turn_temp = each[7]
                turn_temp = format_time(turn_temp)

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

        roast.append(aline)

        for a_record in roast:
            f.write(a_record + '\n')

        f.close()


debug = False
roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
check_db(roastmaster_db)
show_coffee_list()
create_report()
