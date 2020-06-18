# Chromium_Flagged Plotter- Intellus Chromium Data.py

# This code generates figures from all of the files
# in the specified path

# Written by Casey Gierke of Lee Wilson & Associates
# Updated 8/17/2018
# Updated 10/24/2018

# With Notepad++, use F5 then copy this into box
# C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
import pylab
import datetime
from dateutil import parser
from pylab import *
import os
import glob
import pyodbc
# from datetime import datetime
# rcParams['figure.figsize'] = 7, 4

# ------------------------------------------------------
# DEFINE FUNCTIONS
# ------------------------------------------------------

# Define last position finder
def find_last(s,t):
	last_pos = -1
	while True:
		pos = s.find(t, last_pos +1)
		if pos == -1:
			return last_pos
		last_pos = pos

# # Create finder function
# def find_nth(haystack, needle, n):
    # start = haystack.find(needle)
    # while start >= 0 and n > 1:
        # start = haystack.find(needle, start+len(needle))
        # n -= 1
    # return start

def DB_get(SQL):
	db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
						  "Server="+server+";"
						  "Database=Chromium;"
						  "Trusted_Connection=yes;")
	db.autocommit = True

	# Prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor.execute(SQL)
	result = cursor.fetchall()
	db.close()
	return result

def getCredentials():
	credentialsFile = open(path+os.sep+'Python'+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get DB credentials
server = getCredentials()

# DB setup
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
							"Server="+server+";"
							'DATABASE=Chromium;'
							'Trusted_Connection=yes') 

def getCredentials():
	credentialsFile = open(path+os.sep+'Python'+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Read in all file names

# # Create array to store file names
# files = []
# # Get file names
# os.chdir(path)
# for file in glob.glob(path+os.sep+'Data'+os.sep+'txt Files'+os.sep+'*.txt'):
    # files.append(file)

# Make dictionary for appendix figures
figureDict = {}
Dictin = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Locations- Intellus Chromium Data.txt','r')

# # Get first line
# cols = Dictin.readline()
# # cols = cols.replace(' ','_')
# # cols = cols.upper()
# cols = cols.split('\t')
# headers = cols

# # # Get desired indices from header row
# locID_index = headers.index('LOC_LOCATI')
# lat_index = headers.index('LOC_LATITU')
# long_index = headers.index('LOC_LONGIT')
# type_index = headers.index('PZ_AQUIFER')

# Read in data
for line in Dictin:
	Columns = line.split('\t')
	figureDict[Columns[0]] = {'Lat': Columns[1], 'Long': Columns[2][:-1]}

# # Short circuit
# figureDict = {'MCA-2': figureDict['MCA-2']}

# Create an outfile for storing maxes
fout = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Maxes- Intellus Chromium Data.txt','w')

# Create an outfile for storing maxes
foutExceedance = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Exceedance- Intellus Chromium Data.txt','w')

# Create an outfile for defining active locations
foutActive = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Active- Intellus Chromium Data.txt','w')

# Define plotting start and end dates
start = '1/1/1980'
end = '4/30/2020'

# # Create something for naming subplots
# letters = 'abcdefghijklmnopqrstuvwxyz'

# # Convert to numeric for Python to deal with it
# start = parser.parse(start)
# end = parser.parse(end)

# ------------------------------------------------------
# COMPUTATIONS
# ------------------------------------------------------

# # Get length of input files
# n = len(Files)

SLV = 50

# Loop over inputs

for location in figureDict:

	print('Working on '+location)

	# days = []
	# Value = []
	daysND = []
	dataND = []
	daysF = []
	dataF = []

	# Open figure for plotting
	fig = plt.figure()
	
	# Define axis for plotting
	ax1 = fig.add_subplot(111)

	# # Make a variable for naming, pull well name from path
	# inpst = Files[j][Files[j].find('txt Files')+10:Files[j].find('.')]
	
	# if inpst in figureDict:
		# # fig.savefig(path+os.sep+'Figures'+os.sep+'Appendix Figures'+os.sep+figureDict[inpst]+'.png',dpi=500)
		# print('Working on '+Files[j])

	# Open the file to plot
	# fin = open(Files[j])
	# df = pd.read_csv(path+os.sep+'Data'+os.sep+'txt Files'+os.sep+location+'.txt', sep='\t', header=None)
	# Query out data
	# df = pd.read_sql("SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"'", con=sql_conn)
	sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' ORDER BY SAMPLE_DATE"
	data = DB_get(sql)
		
	# df.columns = ['Date', 'Result', 'Detected', 'Filtered']
	# df['Date'] = pd.to_datetime(df['Date'])
	
	# # Sort the date by Date
	# df = df.sort_values(by=['Date'])
	
	# Initialize arrays
	date = []
	result = []
	ND = []
	F = []
	daysND = []
	dataND = []
	daysF = []
	dataF = []

	# for row in df.iterrows():
	for row in data:
	# for line in fin:
		# print(row[1]['Detected'], row[1]['Filtered'])
		# x1 = find_nth(line,'\t',1)
		# x2 = find_nth(line,'\t',2)
		# x3 = find_nth(line,'\t',3)
		
		# days.append(parser.parse(line[:x1]))
		# Value.append(line[x1+1:x2])
		
		date.append(row[0])
		result.append(row[1])
		ND.append(row[2])
		F.append(row[3])
		
		# Check for non-detects
		# if line[x2+1:x3] == 'N':
		if row[2] == 'N':
			daysND.append(row[0])
			dataND.append(row[1])
		# Check for filtering
		# if line[x3+1:-1] == 'Y':
		if row[3] == 'Y':
			daysF.append(row[0])
			dataF.append(row[1])
			# daysF.append(days[-1])
			# # daysF.append(days[-1]-datetime.timedelta(days=60))
			# dataF.append(Value[-1])
	
	# fin.close()
	
	# ------------------------------------------------------
	# OUTPUTS
	# ------------------------------------------------------
	
	# Check if result has values
	if result == []:
		maxResult = 'No Data'
		maxDate = 'No Data'
		maxND = 'No Data'
		maxF = 'No Data'
	else:
		# Get max
		maxResult = max(result)
		maxIndex = result.index(maxResult)
		maxDate = date[maxIndex]
		maxND = ND[maxIndex]
		maxF = F[maxIndex]
	
		# Write exceedances to outfile
		if float(maxResult) > SLV:
			foutExceedance.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')

		# Check if active
		if datetime.datetime(max(date).year, max(date).month, max(date).day) > datetime.datetime.strptime('2015-01-01', '%Y-%m-%d'):
			foutActive.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\n')
		
	# Write maxes to an outfile
	fout.write(location+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')
	
	# lns1 = ax1.plot_date(days, Value, '-', color='#00008B')
	# lns2 = ax1.plot_date(days, Value, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered')
	lns5 = ax1.plot_date([pd.to_datetime(start), pd.to_datetime(end)], [SLV, SLV], '-r', label = 'SLV')
	lns1 = ax1.plot_date(date, result, '-', color='#00008B')
	lns2 = ax1.plot_date(date, result, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered')
	lns3 = ax1.plot_date(daysF, dataF, 'ob', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered')
	# lns3 = ax1.plot_date(daysF, dataF, marker=r"$ {} $".format('F'), color='k', markersize=6, label = 'Filtered')
	lns4 = ax1.plot_date(daysND, dataND, '.r', markersize=2, label = 'Non-Detect')
	
	lns = lns2+lns3+lns4+lns5
	labs = [l.get_label() for l in lns]
	# labs.append('Non-Detect',)
	fig.legend(lns, labs, loc='upper right', fontsize= 7, prop={'size':5}, numpoints=1, framealpha=1)

	# if inpst in figureDict:
	ax1.set_title(location, loc='left', fontsize=8)
		
	ax1.grid(True)

	# Make y axis labels
	ax1.set_ylabel('Chromium [$\mu$g/L]', color='k')
	# pylab.xlim(start,end)         # to control primary x-axis range
	pylab.ylim(0.1,1300)         # to control primary y-axis range
	ax1.set_yscale('log')
	grid(b=True, which='major', color='k', linestyle='-')
	grid(b=True, which='minor', color='grey', linestyle='-', linewidth=0.25)
	
	ax1.xaxis.label.set_color('k')
	ax1.tick_params(axis='y', colors='k')
	ax1.yaxis.set_major_formatter(ScalarFormatter())

	# Rotate x axis labels
	plt.setp( ax1.xaxis.get_majorticklabels(), rotation=35 )
	# Raise up bottom and side to accomodate labels and legend
	plt.subplots_adjust(top=.88, bottom=.2, right=.95)

	# Adjust size of output plots
	font = {'family' : 'Times New Roman',
        'weight' : 'normal',
        'size'   : 9}

	plt.rc('font', **font)
	
	# plt.rcParams["font.size"] = '7'
	# plt.rcParams["font.family"] = 'Times New Roman'
	
	# # Used to throw error and work on output plot
	# lns6 = ax1.plot_date([start,end], [SV, SLV], '-r', label = 'SLV')
	
	# Adjust figure size
	fig.set_size_inches(3.25,1.75)
	fig.subplots_adjust(hspace=.3)
	
	# Check that destination directories exist and create if not
	if not os.path.exists(path+os.sep+'Intellus Data'+os.sep+'Figures'+os.sep+'Intellus Chromium Data'+os.sep):
		os.makedirs(path+os.sep+'Intellus Data'+os.sep+'Figures'+os.sep+'Intellus Chromium Data'+os.sep)

	# fig.savefig(path+os.sep+'Figures'+os.sep+inpst+'.png',dpi=500)
	# fig.savefig(path+os.sep+'Intellus Data'+os.sep+'Figures'+os.sep+'Intellus Chromium Data'+os.sep+figureDict[location]['Aquifer']+'- '+location+'.png',dpi=500)
	fig.savefig(path+os.sep+'Intellus Data'+os.sep+'Figures'+os.sep+'Intellus Chromium Data'+os.sep+location+'.png',dpi=500)
	# if inpst in figureDict:
		# fig.savefig(path+os.sep+'Figures'+os.sep+'Appendix Figures'+os.sep+figureDict[inpst]+'.png',dpi=500)
	
	# plt.show()
	clf()
	plt.close('all')
	# fig.close()

fout.close()
foutExceedance.close()
foutActive.close()