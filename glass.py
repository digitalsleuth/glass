#!/usr/bin/env python3
import os
import hashlib
from sys import argv
import datetime
import pdb
import sqlite3
import datetime
#Check for the magic library.
try:
    import magic 

except ImportError:
    print("python-magic is not installed! \n\
          Install it with pip: \n\
          -  pip install python-magic \n\
          Or go to the Github page: \n\
          - https://github.com/ahupp/python-magic")

try:
    import iosquery


'''The glass.py script will traverse through a phone backup and look for database files. 
It will then open these files up in sqlite 3 and attempt to execute multiple queries. 
The output of each query will be stored in a file that is inside of a new folder made by the script each execution. 

Naming format: [date][root]/[db][query].csv

Example:
June-05-19-zachbackup/glassdoorSELECTcompany.csv
June-07-19-zachbackup/glassdoorJOINnotifications.csv
June-12-19-zachbackup2/glassdoorSELECTtimestamps.csv

Dependencies: 
pip install python-magic'''

def processDirectories(directory) :
    for root, dirs, files in os.walk(directory) :
        filecount = 0
        dbfiles = 0
        for file in files:
            fname = os.path.join(root, file)
            #Check if ftype is a sqlite file.
            m = magic.Magic(mime=True)
            ftype = m.from_file(os.path.abspath(fname))
            if "SQLite 3.x database" in ftype:
                result = runthrough(fname, file)
            else:
                result = False

            if result:
                #What do we want?
                dbfiles += 1
            else:
                filecount += 1
    print("{} files scanned!".format(filecount))
    print("{} database files found!".format(dbfiles))

def runthrough(dbpath, db):
    if os.path.exists(dbpath):
        #Grabs our pre-made select statements.
        if "glassdoor" in dbpath:
            for i in iosquery.SELECT:
                dbexec(db, i)
        else:
            return False
    else:
        return False

def dbexec(db, command):
    #Runs commands on the database.
    #Open db
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        print("{} could not be opened!".format(db))

    #Run command
    #If successful output to csv
    #Filedate is HourMinute
    #Else write to error log
    try:
        output = cursor.execute(command)
        #We have some complex string formatting.
        #Since the queries can contain a * 
        #our dynamic naming options will be limited.
        dirDate = str(datetime.datetime.now()).split(" ")[0]
        dirName = "{}-{}".format(fileDate, directory)
        #example: 2019-06-11-glassdoor
        fileDate =  str(datetime.datetime.now()).split(" ")[1].split(":")[:2]
        fileDate = fileDate[0] + fileDate[1]
        fileCommand = command.split(" ")[:1][0]
        fileName = "{}{}{}".format(db, fileCommand, fileDate)
        with open("{}\\{}.csv".format(dirName, fileName), "rw") as newfile:
            newFile.write(output)
    except:
        #Errlog will be an existing file that we keep adding to
        #Might change this implementation later on if too crowded
        #or purge it after each analysis
        with open("errorlog.csv") as errlog:
            errlog.write("Error with database: {} performing command: {}".format(db, command))
        return False



if __name__ == '__main__' :
    #Grab our arguments. 
    #Script is the name of our script
    #Directory is the name of the directory to start traversal.
    print("Running glass.py v0.0.1")
    script, directory = argv
    processDirectories(directory)
