__author__ = 'Kor'

"""
This program will read from the Roastmaster database and output a menu of the
current roasts
"""

import sqlite3 as lite
import os
import shutil

# import arrow
from datetime import datetime, timedelta
import time

rmDB = 'c:/users/kor/dropbox/apps/roastmaster/My Database.sqlite'


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


def check_db():
    try:

        metadata = os.stat(
            'c:/users/kor/dropbox/apps/roastmaster/My Database.sqlite')
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
        elif choice == 2:

            shutil.copyfile(
                'c:/users/kor/dropbox/apps/roastmaster/My Database.sqlite',
                'd:/development/roastmaster/roast_master.db')
        else:
            print("Keeping current database")


def get_date(timeNow, dateFormat="%d-%m-%Y", addDays=0):
    timeNow = datetime.now()
    # print("timeNow: ", timeNow)
    if (addDays != 0):
        anotherTime = timeNow + timedelta(days=addDays)
    else:
        anotherTime = timeNow

    return anotherTime.strftime(dateFormat)


def show_coffee_list():
    con = lite.connect('D:/development/roastmaster/roast_master.db')

    epoch = datetime(1970, 1, 1)
    year = timedelta(days=365.2425)
    epoch_delta = year * 31
    addDays = 7
    output_format = '%d-%m-%y'
    output = get_date(epoch_delta, output_format, addDays)
    # print(output)



    with con:
        # print("%2s %-10s %s" % d)

        print()
        print()
        row_factory = lite.Row

        cur = con.cursor()
        # SELECT datetime( r.ZDATE, 'unixepoch', '31 YEARS', '+1 day',
        # 'localtime' ) AS Date,

        sql = """
            SELECT datetime( r.ZDATE, 'unixepoch', '31 YEARS', '+1 day',
            'localtime' ) AS Date1,
                   r.ZDATE AS Date2,
                   b.ZMARKETNAME AS [Market Name],
                   b.ZGRADE AS [Grade],
                   ( CAST ( CAST ( r.ZDURATION / 60.0 AS int )  AS string )
                   || ':' || CAST ( ZDURATION % 60 AS string )  ) AS Duration
              FROM (
                (
                        ZROAST r
                               JOIN ZROASTEDITEM i
                                 ON i.ZROAST = r.Z_PK
                    )

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
        col_names = [cn[0] for cn in cur.description]

        print(
            "{0:<19} {1:21}{2:15}{3}".format(col_names[0],
                                             col_names[1], col_names[2],
                                             col_names[3]))

        print('_' * 90)

        # for each in (cur.fetchall()):
        #     for col in each:
        #         if col == None:
        #             col = 'None'
        #
        #         print("{:32}".format(col), end='')
        #     print()
        for each in (cur.fetchall()):
            temp = each[1]
            temp = each[1] + epoch_delta.total_seconds()
            date = time.ctime(temp)

            # temp2 = datetime.strptime("Tue Aug 25 16:02:44 2015", "%a %b %d
            #  %H:%M:%S %Y")
            temp2 = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
            temp3 = temp2.strftime("%a %b %d")
            temp4 = temp2.strftime("%a %b %d")

            print(
                "{0:26}{1:21}{2:15}{3}".format(date, each[0], each[2], each[3]))

        print('_' * 90)


check_db()
show_coffee_list()
