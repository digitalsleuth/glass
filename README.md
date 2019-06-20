# Glass v.0.1.0.1 - A Tool for Automated Glassdoor Analysis

Glass is a python script that traverses through iphone backups to locate sqlite3 database files for the job search application known as "Glassdoor". The program will then attempt to execute pre-made queries on them and parse the output to csv files. The files are generated based on database name, type of command used, and datetime information.

The folder you run the program in will be the one that the reports are sent.

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
- `git clone https://github.com/IronCityCoder/glass.git`
- This makes a new folder called 'glass'
- Use the command `cd glass` to navigate to the tools.

## Running the program

### Windows

- Open up command line and navigate to the directory. 
- `./glass.py [path to directory]`

### Linux

- After following installation, you should already be in the directory.
- Run `chmod +x *` to allow all the files to be run.
- `./glass.py [path to directory]`


## Development

Feel free to submit feedback, bug reports, and your own tweaks to the program! I plan on having a schedule to update this tool, but I will be working on making others in the meanwhile. 

Future goals I have for this are:

- Expand sql queries.
- Create arguments for app type.
 - Rather than just check for glassdoor by default, I'd like to be able to have the user pass in the app they wish to analyze. This would require having multiple files with queries that work for those databases though. 
  - Custom report destinations
 - More options in general, such as specificying output type, running only SELECT statements, etc.
