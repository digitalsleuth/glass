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
    from iosquery import query

except ImportError:
    print("The iosqueries are not in the same directory! \n\
           Please make sure to add them to run the program!")

'''
#The glass.py script will traverse through a phone backup and look for database files. 
#It will then open these files up in sqlite 3 and attempt to execute multiple queries. 
#The output of each query will be stored in a file that is inside of a new folder made by the script each #execution. 

#Naming format: [date][root]/[db][query].csv

#Example:
#2019-5-07-zachbackup/glassdoorSELECTcompany.csv
#2019-6-04-zachbackup/glassdoorJOINnotifications.csv
#2019-6-05-zachbackup2/glassdoorSELECTtimestamps.csv

#Dependencies: 
#pip install python-magic
'''

#This function walks through the direectories to find database files.
def processDirectories(directory):
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
        #print("PATH IS REAL")
        #print(dbpath)
        if "glassdoor" in dbpath.lower():
            for i in query.getSelect():
                dbexec(db, i, os.path.abspath(dbpath))
            return True

        else:
            return False
    else:
        return False

def dbexec(db, command, fullpath):
    #Runs commands on the database.
    #Open db
    #print(os.getcwd())
    try:
        #print('{}'.format(fullpath))
        #print(os.getcwd)
        #print(command)
        conn = sqlite3.connect('{}'.format(fullpath))
        
        #Run command
        #If successful output to csv
        #Filedate is HourMinute
        #Else write to error log
        curr = conn.cursor()
        output = []
        for row in curr.execute(command):
            #print(row)
            output.append(row)

        conn.close()
        #print(output)
        #We have some complex string formatting.
        #Since the queries can contain a * 
        #our dynamic naming options will be limited.
        #also makes the directory
        dirDate = str(datetime.datetime.now()).split(" ")[0]
        dirDesc = str(db.split(" ")[-1].split(".")[0])
        dirName = "{}-{}".format(dirDate, dirDesc)
        try:
            os.mkdir(dirName)
        except FileExistsError:
            print("{} Directory already exists".format(dirName))
        #example: 2019-06-11-glassdoor
        fileDate =  str(datetime.datetime.now()).split(" ")[1].split(":")[:2]
        fileDate = fileDate[0] + fileDate[1]
        fileCommand = command.split(" ")[:1][0]
        fileName = "{}{}{}".format(dirDesc, fileCommand, fileDate)
        #print("{}/{}.csv".format(dirName, fileName))
        with open("{}/{}.csv".format(dirName, fileName), "w+") as newFile:
            for line in output:
                newFile.write(str(line))
    except:
        #Errlog will be an existing file that we keep adding to
        #Might change this implementation later on if too crowded
        #or purge it after each analysis
        with open("errorlog.csv", "w+") as errlog:
            errlog.write("Error with database: {} performing command: {}".format(db, command))



if __name__ == '__main__':
    #Grab our arguments. 
    #Script is the name of our script
    #Directory is the name of the directory to start traversal.
    print("Running glass.py v0.0.1")
    script, directory = argv
    processDirectories(directory)
