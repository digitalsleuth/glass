# iOS Forensic tool for Automated Glassdoor Analysis

Glass is a python script that traverses through phone backups to locate sqlite3 database files for the job search application known as "Glassdoor". The program will then attempt to execute pre-made queries on them and parse the output to csv files stored in a new directory. The directories are dynamically generated based on the datetime and starting folder name while the files are generated based on database name, type of command used, and datetime information.

Dependencies:

- [python-magic](https://github.com/ahupp/python-magic)

## Installing the program

### Windows

- Click "Clone or Download"
- Download ZIP
- Extract ZIP to folder you plan to work in. 
- Open command line.
- Type `pip install python-magic` to ensure dependencies are met.
  - If you have python2 and python3 installed, this might be `pip3 install python-magic`

### Linux

- Open command line.
- Type `pip3 install python-magic` to ensure dependeices are satisfied.
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
 - More options in general, such as specificying output type, running only SELECT statements, etc.
