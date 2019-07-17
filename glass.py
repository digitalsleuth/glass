#!/usr/bin/env python3
import pathlib
from sys import argv
from datetime import datetime as dt
import sqlite3
import math
import argparse

#Check if we have our custom queries.
try:
	from iosquery import query

except ImportError:
	print("The iosqueries are not in the same directory! \n\
		Please make sure to add them to run the program!")

'''
Glass is a python script that traverses through iphone backups
to locate sqlite3 database files for the job search 
application known as "Glassdoor". 

The program will then attempt to execute pre-made queries 
and parse the output to csv files. 

The folder you run the program in will hold the reports.

./glass.py [path] -m
'''
#Open up our queries file.
def openQueries():
	query = []
	with open("queries/iosquery.csv", "r+") as iosquery:
		for row in iosquery:
			for command in row.split(","):
				query.append(command.strip())
	return query
			 

#Quick function to log errors.
def logerror(message):
	with open("errorlog.csv", "w+") as errlog:
		errlog.write(message)

#Uses pathlib's rglob function to search fstrings for files that have keyword in them.
def pattern(keyword, extension, pathObj):
	filegrab = pathObj.rglob(f"*.{extension}")
	matches = []
	for file in filegrab:
		if f"{keyword}" in str(file).lower():
			matches.append(str(file))
	return matches


#We find all glassdoor databases along a path.
def crawl(directory):
	path = pathlib.Path(directory)
	
	#Search for db and sqlite files.
	sqlitedb = pattern(keyword, "sqlite", path)
	regulardb = pattern(keyword, "db", path)

    	dbs = sqldb + normdb #Store all the matches in a list.
	return dbs

#Cycles through every db found and running queries against it.
def runThrough(dbs):
	for count, file in enumerate(dirs):
		progress = math.floor((count / len(dirs)) * 100))
		print(f"{progress}% of the way done")
		#Iterate over our pre-made queries.
		for query in openQueries():
			DBexec(file, query)
	       
	 print(f"{} database files found!")

#Returns an opened database object.
#If fails we log an error.
def dbConnect(db):
	try:
		conn = sqlite3.connect('{}'.format(db))
		curr = conn.cursor()
		return curr
	except:
		logerror(f"Error opening database: {db}!")

#Using string formatting to create a name for our results.
def generateName(db, command):
	date = dt.now()
	filedate = f"{date.day}-{date.month}-{date.year}"
	command = command.split(" ")[:1][0]
	return f"{keyword}{command}{date}"

#Try to open the database file.
#If successful it will pass a query.
#Otherwise an error will be logged.
def DBexec(db, command):
	dbcurr = dbConnect() #Db object
	filename = generateName(db, command)

	#Open a file and write the command output to it.
	with open(f"{filename}.csv", "w+") as outputfile:
	    for row in curr.execute(command):
		newFile.write(str(row))  
	    conn.close()

	except:
	logerror("Error with database: {} performing command: {}".format(db, command))

## EACH FUNCTION SHOULD DO ONE THING. CRAWL SHOULD JUST CRAWL AND RETURN ALL DBs.

#Manually interacting with the database.
def manualMode(path):
	pass

#We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Glass 1.0.3 is a tool for interacting with glassdoor databases.')
	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('path', help="Path: The path files will be read or scanned from.")
	group.add_argument('-m', action= "store_true", help="Manual interaction with databases.)
	args = parser.parse_args()
	
	global keyword	
	keyword = "glassdoor" #Could make this a command line arg.
	
	if args.m:
		manualMode(path)
	else:
		dbs = crawl(path)
		runThrough(dbs)

'''
LOGIC
IF m flag (manual db)
PRINT numbered list of datbases found
User inputs the number of a DB or 0 to exit
TRY query
IF SUCCESSFUL save query and print output
'''


