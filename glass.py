#!/usr/bin/env python3

'''
Glass is a python script that traverses through iphone backups
to locate sqlite3 database files for the job search 
application known as "Glassdoor". 

The program will then attempt to execute pre-made queries 
and parse the output to csv files. 

The folder you run the program in will hold the reports.

./glass.py [path] -m
'''

import pathlib
from sys import argv
from datetime import datetime as dt
import sqlite3
import math
import argparse

# Open up our queries file.
def open_queries():
	query = []
	with open("queries/iosquery.csv", "r+") as iosquery:
		for row in iosquery:
			for command in row.split(","):
				query.append(command.strip())
	return query
			 
def write_queries(command):
	with open("queries/iosquery.csv", "w+") as iosquery:
		iosquery.write(f"{command},")

# Quick function to log errors.
def log_error(message):
	with open("errorlog.csv", "w+") as errlog:
		errlog.write(message)

# Uses pathlib's rglob function to search fstrings for files that have keyword in them.
def pattern(keyword, extension, pathObj):
	file_grab = pathObj.rglob(f"*.{extension}")
	matches = []
	for file in file_grab:
		if f"{keyword}" in str(file).lower():
			matches.append(str(file))
	return matches


# We find all glassdoor databases along a path.
def crawl(directory):
	path = pathlib.Path(directory)
	
	# Search for db and sqlite files.
	sqlite_db = pattern(keyword, "sqlite", path)
	regular_db = pattern(keyword, "db", path)

    	dbs = sqldite_b + regular_db  # Store all the matches in a list.
	return dbs

# Cycles through every db found and running queries against it.
def run_through(dbs):
	for count, file in enumerate(dbs):
		progress = math.floor((count / len(dbs)) * 100))
		print(f"{progress}% of the way done")
		# Iterate over our pre-made queries.
		for query in open_queries():
			db_exec(file, query)
	       
	 print(f"{} database files found!")

# Returns an opened database object.
# If fails we log an error.
def db_connect(db):
	try:
		conn = sqlite3.connect('{}'.format(db))
		curr = conn.cursor()
		return [curr, conn]
	except:
		log_error(f"Error opening database: {db}!")

# Using string formatting to create a name for our results.
def generate_name(db, command):
	date = dt.now()
	filedate = f"{date.day}-{date.month}-{date.year}"
	command = command.split(" ")[:1][0]
	return f"{keyword}{command}{date}"

# Try to open the database file.
# If successful it will pass a query.
# Otherwise an error will be logged.

### Might want to generalize this and write output in a different function ###
### - write_report() ?

def db_exec(db, command):
	db_obj = db_connect() # Db object
	curr = db_obj[0]
	filename = generate_name(db, command)

	# Open a file and write the command output to it.
	with open(f"{filename}.csv", "w+") as output_file:
            try:
	    	for row in curr.execute(command):
	            output_file.write(str(row))  
            except:
                log_error(f"Error with running {command} on {db}")

	db_obj[1].close()  # Close the database


# Manually interacting with the database.
def display_db(dbs):
	common_names = []
	for count, file in enumerate(dbs):
		path = pathlib.Path(file)
		common_names.append(path.name)
		print(f"{count}|{path.name}")
	return common_names

#Command input.
def manual_db(database, common_name):
	db_obj = db_connect(database)
	curr = db_obj[0]
	conn = db_obj[1]
	print("Connected successfully to {database}")
	while True:
		response = input("{common_name}> ")
		try:
			query = curr.execute(response)
			for row in query:
				print(row)
			write_queries(query)
			
		except:
			log_error(f"{response} did not work.")
		

# Main loop for manual mode.
# User will input a number of a database.
# They can then access that db.
def manual_mode(path):
	print("Manual Mode selected. Please wait for crawling to finish.")
	dbs = crawl(path)
	print("Crawling finished.")
	while True:
		response = input("Please enter the number of the db you want to access or 'quit' to exit.")
		common_names = display_db(dbs)
		if response.lower() == "quit":
			sys.exit()
		elif int(response) in range(len(dbs)):
			manual_db(dbs[int(response), common_names[int(response)])
		else:
			print("Invalid response.")



# We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Glass 1.0.3 is a tool for interacting with glassdoor databases.')
	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('path', help="Path: The path files will be read or scanned from.")
	group.add_argument('-m', action= "store_true", help="Manual interaction with databases.)
	args = parser.parse_args()
	
	global keyword	
	keyword = "glassdoor"  # Could make this a command line arg.
	
	if args.m:
		manual_mode(path)
	else:
		dbs = crawl(path)
		run_through(dbs)




