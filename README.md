# Glass - A Tool for Automated Glassdoor Analysis

[![version](https://img.shields.io/badge/Version-1.0.3-blue.svg)](https://github.com/IronCityCoder/hasher)
[![stability](https://img.shields.io/badge/stability-stable-green.svg)](https://github.com/IronCityCoder/hasher)

Glass is a python script that traverses through iphone backups to locate sqlite3 database files for the job search application known as "Glassdoor". The program will then attempt to execute pre-made queries on them and parse the output to csv files. The files are generated based on database name, type of command used, and datetime information.

The folder you run the program in will be the one that the reports are sent.

Manual mode can be enabled with the "-m" flag. This will display a list of databases and let you select one.
Once you are inside of the database, you may send it commands, return to the main list with ".list", view tables in the database with ".table", or quit with ".quit"

Dependencies:

- [pathlib](https://docs.python.org/3.7/library/pathlib.html)

## Installing the program

### Windows

- Click "Clone or Download"
- Download ZIP
- Extract ZIP to folder you plan to work in. 
- Open command line.

### Linux

- Open command line.
- Navigate to the directory you want to work in.
- `git clone https://github.com/steelsleuth/glass.git`
- This makes a new folder called 'glass'
- Use the command `cd glass` to navigate to the tools.

## Running the program

### Windows

- Open up command line and navigate to the directory. 
- `./glass.py [path to directory] [-m]`

### Linux

- After following installation, you should already be in the directory.
- Run `chmod +x *` to allow all the files to be run.
- `./glass.py [path to directory] [-m]`


## Development

Feel free to submit feedback, bug reports, and your own tweaks to the program! I plan on having a schedule to update this tool, but I will be working on making others in the meanwhile. 
