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
Glass is a python script that traverses through iphone backups to locate sqlite3 database files 
for the job search application known as "Glassdoor". 
The program will then attempt to execute pre-made queries on them and parse the output to csv files. 
The files are generated based on database name, type of command used, and datetime information.

The folder you run the program in will be the one that the reports are sent.

Dependencies:
    pathlib

Naming format: [db][query][time].csv
Example:
 - glassdoorSELECT2015 (20 hours / 15 minutes)
'''
#Quick function to log errors.
def logerror(message):
  with open("errorlog.csv", "w+") as errlog:
    errlog.write(message)

#Crawl uses pathlib to find all database files.
#We then call runthrough which tries to open them up.
def crawl(directory):
    #if "glassdoor" in str(i).lower()
    path = pathlib.Path(directory)
    #Search for db and sqlite files.
    #Could probably have a function iterate 
    #over a list of common extensions.
    sqldb = [str(x) for x in path.rglob("*.sqlite") if "glassdoor" in str(x).lower()]
    normdb = [str(x) for x in path.rglob("*.db") if "glassdoor" in str(x).lower()]
    #Store our db files in a list.
    #print(sqldb)
    dirs = sqldb + normdb
    dbfiles = len(dirs)
    count = 0
    for file in dirs:
        count += 1
        print("{}% of the way done".format(math.floor((count / dbfiles) * 100)))
        #Iterate over our pre-made queries.
        for i in query.getSelect():
          dbexec(file, i)
       
    print("{} database files found!".format(dbfiles))

#dbexec will open up a database using sqlite3 and execute an argument passed to it.
#any errors will be logged to an error file.
#Filedate is based on HourMinute
def dbexec(db, command):
    try:
        conn = sqlite3.connect('{}'.format(db))
        curr = conn.cursor()

        #Some messy directory formatting to get what we want.
        dirDesc = str(db.split(" ")[-1].split(".")[0]).split("/")[-1]
        #print("Dirdesc: {}".format(dirDesc))
        fileDate =  str(datetime.datetime.now()).split(" ")[1].split(":")[:2]
        fileDate = fileDate[0] + fileDate[1]
        fileCommand = command.split(" ")[:1][0]
        fileName = "{}{}{}".format(dirDesc, fileCommand, fileDate)
        #print("FileName: {}".format(fileName))
        #Open a file and write the command output to it.
        with open("{}.csv".format(fileName), "w+") as newFile:
            for row in curr.execute(command):
                newFile.write(str(row))  
            conn.close()
    
    except:
        logerror("Error with database: {} performing command: {}".format(db, command))

#We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
    print("Running glass.py v0.1.0.1")
    script, directory = argv
    crawl(directory)
