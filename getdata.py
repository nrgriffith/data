# -*- encoding: utf-8 -*-
from parfile import startDate, DATA
from os import listdir
from os.path import isfile, join
from datetime import datetime as date
from sys import exit

###### Parameters -- CHANGE AS NEEDED! #####
pathName = "../pulled-data" # Local path name
outputFile = DATA # File name to write to
nFiles = 15558 # Known number of file
skipN = 12 # Number of lines to skip
dateChars = 10 # Number of characters in date format
dateFormat = "%Y_%m_%d" # Format of date
startDate = date.strptime(startDate.replace("-", "_"), dateFormat) # Date experiment began
answer = ""

# Get list of file names
fileNames = [f for f in listdir(pathName) if isfile(join(pathName, f))]
fileNames.sort()

# Safety Check -- Make sure correct number of files were found
# If you don't know the number of files, delete/comment-out this portion
if len(fileNames) == nFiles:
    print "Found %d of %d files." %(len(fileNames), nFiles)
else:
    message = "Error: only found %d of %d files." %(len(fileNames), nFiles)
    exit(message)

# Safety Check -- Re-write pre-existing file?
if isfile(outputFile):
    while not (answer == "y" or answer == "Y"):
        print "Warning: %s already exists. Re-write? [y/n]:" %outputFile,
        answer = raw_input()
        if answer == "n" or answer == "N":
            exit("Please change parameters and try again.")

# Open outputFile
compdata = open(outputFile, 'w+')

# Traverse list of file names,
# Store the first dateChars of each file name as a date object,
# Compare each date to start date, ignore files before the start date,
# Check to ensure the file isn't empty,
# Skip the first skipN lines of each approved file,
# Write remaining lines to outputFile,
# Close outputFile
for i in fileNames:
    currentDate = i[:dateChars]
    currentDate = date.strptime(currentDate, dateFormat)
    if currentDate >= startDate:
        f = open(join(pathName, i), 'r')
        f.seek(0)
        if f.read(1):
            for n, line in enumerate(f):
                if n >= skipN and line.strip() != "":
                    compdata.write(line)
            else:
                compdata.write('\n')
        f.close()
compdata.close()

# Print confirmation message
print "Okay done!"
