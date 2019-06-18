#!/usr/bin/env python3
import os
from sys import argv
import datetime
import sqlite3

#Check for the magic library that identifies file types.
try:
    import magic 

except ImportError:
    print("python-magic is not installed! \n\
          Install it with pip: \n\
          -  pip install python-magic \n\
          Or go to the Github page: \n\
          - https://github.com/ahupp/python-magic")

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

#Crawl walks through the direectories to find database files.
#It uses magic.Magic to check the filetype.
#Right now we are checking if the file is "SQLite 3.x" but we can add more checks.
def crawl(directory):
    for root, dirs, files in os.walk(directory):
        filecount = 0
        dbfiles = 0
        for file in files:
            fname = os.path.join(root, file)
            #Check if ftype is a sqlite file.
            #If mime is true we need another condition to check for.
            m = magic.Magic(mime=False)
            ftype = m.from_file(os.path.abspath(fname))
            if "SQLite 3.x" in ftype:
                result = runthrough(fname, file)
            else:
                result = False
            
            #We can keep track of how many files we found that match what we are looking for.
            if result:
                dbfiles += 1
            else:
                filecount += 1
                
    print("{} files scanned!".format(filecount))
    print("{} database files found!".format(dbfiles))

def runthrough(dbpath, db):
    if os.path.exists(dbpath):
        #Verify that the target is a glassdoor database.
        if "glassdoor" in dbpath.lower():
            #Iterate over our pre-made queries.
            #We can return true to track our count of databases.
            for i in query.getSelect():
                dbexec(db, i, os.path.abspath(dbpath))
            return True
    #If neither if statement is true, then we can return False by default.
    return False

#dbexec will open up a database using sqlite3 and execute an argument passed to it.
#any errors will be logged to an error file.
#Filedate is based on HourMinute
def dbexec(db, command, fullpath):
    try:
        conn = sqlite3.connect('{}'.format(fullpath))
        curr = conn.cursor()

        #Some messy directory formatting to get what we want.
        dirDate = str(datetime.datetime.now()).split(" ")[0]
        dirDesc = str(db.split(" ")[-1].split(".")[0])
        dirName = "{}-{}".format(dirDate, dirDesc)
        
        #Make a new directory to store the output in.
        try:
            os.mkdir(dirName)
        except FileExistsError:
            #Folder already exists so nothing to do.
            pass

        fileDate =  str(datetime.datetime.now()).split(" ")[1].split(":")[:2]
        fileDate = fileDate[0] + fileDate[1]
        fileCommand = command.split(" ")[:1][0]
        fileName = "{}{}{}".format(dirDesc, fileCommand, fileDate)
        
        #Open a file and write the command output to it.
        with open("{}/{}.csv".format(dirName, fileName), "w+") as newFile:
            for row in curr.execute(command):
                newFile.write(str(row))
                
        conn.close()
    except:
        with open("errorlog.csv", "w+") as errlog:
            errlog.write("Error with database: {} performing command: {}".format(db, command))

#We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
    print("Running glass.py v0.0.1")
    script, directory = argv
    crawl(directory)
