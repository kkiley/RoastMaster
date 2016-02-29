__author__ = 'Kor'

import msvcrt
import arrow
import sqlite3 as lite
import os
import shutil
import subprocess
import time


"""
This program will read from the Roastmaster database and output data to a text file for
Pusstoe to paste into roastmaster
"""


def create_report():
    print("In create_report")
    # source_file_name = "temp.txt"
    source_file_name = "../temp.txt"
    # source_file_name = "d:/Development/RoastMaster/temp.txt"
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

    print("In check_db")

    woofie_dropbox = 'C:/Users/kiley_000/Dropbox/Apps/Roastmaster/My Database.sqlite'
    tubby_dropbox = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'

    try:
        metadata = os.stat(mydb) #check My Database.sqlite on dropbox
    except IOError:
        print("File does not exist. Correct the problem and restart.")

    if not os.path.isfile('../roast_master.db'):
        shutil.copyfile(
                        mydb,
                        '../roast_master.db')
    else:

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

                shutil.copyfile(
                    mydb,
                    '../roast_master.db')
            else:
                print("Keeping current database")


def get_phase_percent(begin_time, end_time, roast_duration):
    stage_duration = end_time - begin_time
    return '{:.0%}'.format(stage_duration / roast_duration)


def format_time(target_time):
    return time.strftime("%M:%S", time.gmtime(target_time))


def show_coffee_list():
    print("In show_coffee_list")
    con = lite.connect('../roast_master.db')
    # con = lite.connect('D:/development/roastmaster/roast_master.db')
    f = open('../temp.txt', "w")
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
    ORDER BY zduration DESC;
           """
        previous_roast = ''
        roast = []
        oldtime = ''
        begun = False

        cur.execute(sql, (time_interval, unix_epoch))

        aline = arrow.now().format('dddd MMMM D') + ' - '  + "Roasts that will be displayed on Coffee Menu"
        f.write(aline + '\n\n')

        col_names = [cn[0] for cn in cur.description]

        aline = "{0:<19} {1:15} {2:12}".format(col_names[0], col_names[1], col_names[2])
        for name in col_names:
            print(':' + name)

        for each in (cur.fetchall()):

            # UNIX epoch is 31 years and 1 day earlier than Code Data time
            # Format date():
            temp = arrow.Arrow.fromtimestamp(each["Roast Date"])
            print(temp)
            date = temp.replace(years=31, days=1)
            date = date.format('MM/DD/YY hh:mm')

            # aline = (
            #     "{0:}, {1:}, {2:}".format(date,
            #          each["Country of Origin"], each["Market Name"]))
            aline = (
                "{0:}, {1:}".format(date,
                      each["Market Name"]))
            # print(aline)
            if date != oldtime:
                roast.append(previous_roast)
                previous_roast = aline
                oldtime = date

            previous_roast = aline

        roast.append(aline)

        for a_record in roast:
            f.write(a_record + '\n')

        f.close()

if __name__ == '__main__':
    debug = False
    roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
    # roastmaster_db = 'C:/Users/kiley_000/Dropbox/Apps/Roastmaster/My Database.sqlite'
    check_db(roastmaster_db)
    show_coffee_list()
    create_report()
    print("...push any key to exit")
    inp = msvcrt.getch()
    # os.system('Pause')
