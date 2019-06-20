#!/usr/bin/env python3
import pathlib
from sys import argv
import datetime
import sqlite3
import math

#Check if we have our custom queries.
try:
    from iosquery import query

except ImportError:
    print("The iosqueries are not in the same directory! \n\
           Please make sure to add them to run the program!")

'''
#The glass.py script will traverse through a phone backup and look for database files. 
#It will then open these files up in sqlite3 and attempt to execute queries. 
#The output of each query will be stored in a file that is inside of a new folder.
#If a query causes an error, rather than a new file being made, the output will go to an error log.

#Naming format: [date][root]/[db][query].csv

#Example:
#2019-5-07-zachbackup/glassdoorSELECT.csv
#2019-6-04-zachbackup/glassdoorJOIN.csv
#2019-6-05-zachbackup2/glassdoorSELECT.csv

#Dependencies: 
#pip install python-magic
'''
#Quick function to log errors.
def logerror(message):
  with open("errorlog.csv", "w+") as errlog:
    errlog.write(message)

dirs = []
#Function to grab dbpaths out of a pathlib object.
def grabdb(obj):
  for i in obj:
    #Verify that the target is a glassdoor database.
    if "glassdoor" in str(i).lower():
      dirs.append(str(i))

#Crawl uses pathlib to find all database files.
#We then call runthrough which tries to open them up.
def crawl(directory):
    #Globals
    path = pathlib.Path(directory)
    fname = ''
    ftype = ''
    #Search for db and sqlite files.
    #Could probably have a function iterate 
    #over a list of common extensions.
    sqldb = path.rglob("*[glassdoor]*.sqlite")
    normdb = path.rglob("*[glassdoor]*.db")
    #Store our db files in a list.
    grabdb(sqldb)
    grabdb(normdb)

    dbfiles = len(dirs)
    count = 0
    for file in dirs:
        count += 1
        print("{}% of the way done".format(math.floor((count / dbfiles) * 100)))
        #Might have to pull the file name itself out for dir creation.
        runthrough(file)
       
    print("{} database files found!".format(dbfiles))

def runthrough(db):
    #Iterate over our pre-made queries.
    for i in query.getSelect():
        dbexec(db, i)

#dbexec will open up a database using sqlite3 and execute an argument passed to it.
#any errors will be logged to an error file.
#Filedate is based on HourMinute
def dbexec(db, command):
    try:
        conn = sqlite3.connect('{}'.format(db))
        curr = conn.cursor()

        #Some messy directory formatting to get what we want.
        dirDesc = str(db.split(" ")[-1].split(".")[0]).split("/")[-1]
        print("Dirdesc: {}".format(dirDesc))
        fileDate =  str(datetime.datetime.now()).split(" ")[1].split(":")[:2]
        fileDate = fileDate[0] + fileDate[1]
        fileCommand = command.split(" ")[:1][0]
        fileName = "{}{}{}".format(dirDesc, fileCommand, fileDate)
        print("FileName: {}".format(fileName))
        #Open a file and write the command output to it.
        with open("{}.csv".format(fileName), "w+") as newFile:
            for row in curr.execute(command):
                newFile.write(str(row))
                
        conn.close()
    except:
        logerror("Error with database: {} performing command: {}".format(db, command))

#We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
    print("Running glass.py v0.1.0.0")
    script, directory = argv
    crawl(directory)
