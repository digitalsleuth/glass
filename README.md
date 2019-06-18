# iOS Forensic tool for Automated Glassdoor Analysis

Glass is a python script that traverses through phone backups to locate sqlite3 database files. The program will then attempt to execute pre-made queries on them and parse the output to csv files stored in a new directory. The directories are dynamically generated based on the datetime and starting folder name while the files are generated based on database name, type of command used, and datetime information.

Dependencies:

- [python-magic](https://github.com/ahupp/python-magic)
