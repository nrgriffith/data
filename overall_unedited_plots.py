from parfile import startDate, endDate, dateFormat
from os.path import isfile
from sys import exit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from datetime import datetime as date

###################### Parameters ######################
DATA = "data.txt" # File that stores the data
figGridRow = 3 # Number of rows in each figure
figGridCol = 1 # Number of cols in each figure
days = mdates.DayLocator()
months = mdates.MonthLocator()
monthsFormat = mdates.DateFormatter('%b')
size = 20 # Window size for moving average
numPlots = 3 # Number of plots per figure

startDate = date.strptime(startDate + " 00:00:00", dateFormat)
endDate = date.strptime(endDate + " 00:00:00", dateFormat)
#########################################################

###################### Data Format ######################
# Each line in data.txt is presented like this:
# int, date, time, int, int, A1, A2, A3, B1, B2, B3, C1, C2, C3
# Not interested in the int values at this time.
#########################################################

###################### Data Lists #######################
# Store lists of tuples
A = []
B = []
C = []
#########################################################

####################### Functions #######################
# Moving Average
def MovAvg(var, size):
    fil = np.ones(int(size))/float(size)
    return np.convolve(var, fil, 'same')

# Make figures and subplots
def MakeFig(figNum, title, ymin = [], ymax = [], Y = []):
    fig = plt.figure(figNum)
    fig.suptitle(title)
    x = []
    for each in Y:
        dateVal = date.strptime(each[0], dateFormat)
        x.append(dateVal)
    for n in range(numPlots):
        yVar = [yVar[n+1] for yVar in Y]
        yVarAvg = MovAvg(yVar, size)
        ax = fig.add_subplot(figGridRow, figGridCol, n+1)
        ax.scatter(x, yVar, color="black", marker=".")
        ax.plot(x, yVarAvg, "r")
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFormat)
        ax.xaxis.set_minor_locator(days)
        ax.set_xlim(startDate, endDate)
        ax.format_xdata = mdates.DateFormatter(monthsFormat)
        ax.set_ylim(ymin[n], ymax[n])

#########################################################

# Safety check - Exit if file isn't found
if not isfile(DATA):
    exit("Error locating file. Please check file name and edit parameters.")

# Import data
with open(DATA, "rb") as f:
    lineReader = csv.reader(f, delimiter=",")
    for row in lineReader:
        dateVal = row[1]
        timeVal = row[2]
        timeVal = timeVal[:-2] # Remove the ".1" portion from the time stamp
        A.append(((dateVal+" "+timeVal), float(row[5]), float(row[6]), float(row[7])))
        B.append(((dateVal+" "+timeVal), float(row[8]), float(row[9]), float(row[10])))
        C.append(((dateVal+" "+timeVal), float(row[11]), float(row[12]), float(row[13])))

# Plot As
yMin = [0, 0, 0]
yMax = [75, 80, 65]
MakeFig(1, "A1, A2, and A3", yMin, yMax, A)

# Plot Bs
yMin = [0, 0, 0]
yMax = [80, 80, 80]
MakeFig(2, "B1, B2, and B3", yMin, yMax, B)

# Plot Cs
yMin = [0, 0, 0]
yMax = [80, 80, 80]
MakeFig(3, "C1, C2, and C3", yMin, yMax, C)

plt.show()
