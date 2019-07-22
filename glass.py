#!/usr/bin/env python3

'''
Glass is a python script that traverses through iphone backups
to locate sqlite3 database files for the job search 
application known as "Glassdoor". 

The program will then attempt to execute pre-made queries 
and parse the output to csv files. 

The folder you run the program in will hold the reports.

./glass.py [path] -m

#Add function for manual:
- up arrow lets you cycle through previous commands
- store command history
'''

import pathlib
from sys import argv
from datetime import datetime as dt
import sqlite3
import math
import argparse
import sys

### FILE OPERATIONS
# Open up our queries file.
def open_queries():
	query = []
	with open("queries/iosquery.csv", "r+") as iosquery:
		for row in iosquery:
			for command in row.split(","):
				if len(command.strip()) > 0:
					query.append(command.strip())
	return query

# Checking for duplicates before appending new sql commands to file.			 
def write_queries(command):
	with open("queries/iosquery.csv", "r+") as iosquery:
		for line in iosquery:
			if command in line:
				return

	with open("queries/iosquery.csv", "a") as iosquery:
		iosquery.write(f"{command},")

# Quick function to log errors.
def log_error(message):
	with open("errorlog.csv", "a") as errlog:
		errlog.write(f"{dt.now()}{message}\n")

# Handles query output to file.
def auto_report(db, db_response, query):
	filename = generate_name(db, query)
	#print(db_response)
	# Open a file and write the command output to it.
	with open(f"reports/{filename}.csv", "w+") as output_file:
		for row in db_response:
				output_file.write(str(row)) 	

### UTILITIES
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

	dbs = sqlite_db + regular_db  # Store all the matches in a list.
	return dbs

# Will display a list of found dbs.
def display_db(dbs):
	common_names = []
	for count, file in enumerate(dbs):
		path = pathlib.Path(file)
		common_names.append(path.name)
		print(f"{count}|{path.name}")
	return common_names

# Using string formatting to create a name for our results.
def generate_name(db, command):
	date = dt.now()
	filedate = f"{date.day}-{date.month}-{date.year}-{date.hour}-{date.hour}-{date.minute}"
	command = command.split(" ")[:1][0]
	#print(filedate)
	return f"{keyword}{command}{filedate}"

# Returns an opened database object.
# If fails we log an error.
def db_connect(db):
	try:
		conn = sqlite3.connect(f'{db}')
		curr = conn.cursor()
		return [curr, conn]
	except:
		log_error(f"Error opening database: {db}!")

def sqlite_tables(db):
	table = "SELECT name FROM sqlite_master WHERE type='table';"
	resp = db_exec(db, table)
	for row in resp:
		print(str(row))

# Try to open the database file.
# If successful it will pass a query.
# Otherwise an error will be logged.
def db_exec(db, command):
	db_obj = db_connect(db) #Db object
	curr = db_obj[0]
	conn = db_obj[1]
	try:
		response = [str(x) for x in curr.execute(command)]
		conn.close()
		return response
	except:
		log_error(f"Error with running {command} on {db}")
	#conn.close()  # Close the database


### AUTO MODE
# Cycles through every db found and running queries against it.
def run_through(dbs):
	for count, database in enumerate(dbs):
		progress = math.floor((count / len(dbs)) * 100)
		print(f"{progress}% of the way done")
		# Iterate over our pre-made queries.
		for query in open_queries():
			#print(f"QUERY: {query}")
			response = db_exec(database, query)
			if not(response is None):
				auto_report(database, response, query)    
	print(f"{len(dbs)} database files found!")

### MANUAL MODE
# manual_db allows the user to send commands to the db.
# Will try to re-create some functionality.
def manual_db(database, common_name, path, dblist):
	print(f"Connected to {database}")
	while True:
		response = input(f"{common_name}> ")
		if response == ".quit":
			print("Quitting the program.")
			sys.exit()
		elif response == ".list":
			manual_loop(dblist, path)
		elif response == ".table":
			sqlite_tables(database)
		else:
			# If the response is not a keyword we defined
			# We will try to run it as a sqlite3 query.
			try:
				query = db_exec(database, response)
				for row in query:
					print(str(row))
				write_queries(response)
				
			except:
				log_error(f"{response} did not work.")


# Main loop for manual mode.
# User will input a number of a database.
# They can then access that db.
def manual_loop(dbs, path):
	while True:
		common_names = display_db(dbs)
		response = input("Please enter the number of the db you want to access or 'quit' to exit.\n")
		if response.lower() == ".quit":
			sys.exit()
		# Need to add checks in the future for if they are entering actual integers.
		elif int(response) in range(len(dbs)):
			manual_db(dbs[int(response)], common_names[int(response)], path, dbs)
		else:
			print("Invalid response.")

# Initalizes a list of databases then calls manual_loop.
def manual_mode(path):
	print("Manual Mode selected. Please wait for crawling to finish.")
	dbs = crawl(path)
	print("Crawling finished.")
	if len(dbs) == 0:
		print("No databases found. Closing program.")
		sys.exit()
	manual_loop(dbs, path)




# We could add a menu here depending on how we want to expand the program. 
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Glass 1.0.3 is a tool for interacting with glassdoor databases.')
	parser.add_argument('path', help="Path: The path files will be read or scanned from.")
	parser.add_argument('-m', action= "store_true", help="Manual interaction with databases.")
	args = parser.parse_args()
	
	global keyword	
	keyword = "glassdoor"  # Could make this a command line arg.
	
	if args.m:
		manual_mode(args.path)
	else:
		dbs = crawl(args.path)
		run_through(dbs)




