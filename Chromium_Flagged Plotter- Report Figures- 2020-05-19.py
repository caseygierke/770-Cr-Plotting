# Chromium_Flagged Plotter- Report Figures.py

# This code generates figures from all of the files
# in the specified path

# Written by Casey Gierke of Lee Wilson & Associates
# Updated 8/17/2018
# Updated 10/24/2018
# Updated 4/8/2020
# Updated 5/13/2020

# With Notepad++, use F5 then copy this into box
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

# Adjust size of output plots
font = {'family' : 'Times New Roman',
	'weight' : 'normal',
	'size'   : 12}

plt.rc('font', **font)

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

# Define input file
# input = 'Compiled- Narrowed'
# input = 'Plume- Compiled- Regional'
inputPath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Tables'+os.sep

# Get all the files to plot
files = []
for file in glob.glob(inputPath+"*.txt"):
    files.append(file)

# # Short Circuit
# files = [files[1]]

# Loop through files for plotting different parts
for file in files:

	# Make dictionary for appendix figures
	figureDict = {}
	# Dictin = open(inputPath+input+'.txt','r')
	Dictin = open(file,'r')

	# Get input from file
	input = file[find_last(file,os.sep)+1:-4]
	
	# # Get first line
	# cols = Dictin.readline()
	# cols = cols.split('\t')
	# headers = cols

	# # # Get desired indices from header row
	# locID_index = headers.index('Location ID')
	# lat_index = headers.index('Latitude')
	# long_index = headers.index('Longitude')
	# type_index = headers.index('Aquifer')

	# Read in data
	for line in Dictin:
		columns = line.split('\t')
		figureDict[columns[0]] = {'Lat': columns[2], 'Long': columns[3], 'Aquifer': columns[1]}
		
	# # Short circuit
	# figureDict = {'SIMR-2': figureDict['SIMR-2']}

	# # Create an outfile for storing maxes
	# fout = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Maxes- '+input+'.txt','w')

	# # Create an outfile for storing maxes
	# foutExceedance = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Exceedance- '+input+'.txt','w')

	# # Create an outfile for defining active locations
	# foutActive = open(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Active- '+input+'.txt','w')

	# Define plotting start and end dates
	start = '1/1/1980'
	end = '4/30/2020'

	# ------------------------------------------------------
	# COMPUTATIONS
	# ------------------------------------------------------

	# Define SLV value
	SLV = 7.48

	# Initiate a figure number counter
	figureNumber = 1
	
	# Loop over inputs
	for location in figureDict:

		print('Working on '+location)

		# Open figure for plotting
		fig = plt.figure()
		
		# Define axis for plotting
		ax1 = fig.add_subplot(111)

		# Query out data
		sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND PARAMETER_CODE = 'Cr' ORDER BY SAMPLE_DATE"
		data = DB_get(sql)
			
		# Initialize arrays
		date = []
		result = []
		ND = []
		F = []
		daysND = []
		dataND = []
		daysF = []
		dataF = []

		# Loop through data
		for row in data:
			
			# Append values
			date.append(row[0])
			result.append(float(row[1]))
			ND.append(row[2])
			F.append(row[3])
			
			# Check for non-detects
			if row[2] == 'N':
				daysND.append(row[0])
				dataND.append(float(row[1]))
			# Check for filtering
			if row[3] == 'Y':
				daysF.append(row[0])
				dataF.append(float(row[1]))
		
		# ------------------------------------------------------
		# OUTPUTS
		# ------------------------------------------------------
		
		# # Check if result has values
		# if result == []:
			# maxResult = 'No Data'
			# maxDate = 'No Data'
			# maxND = 'No Data'
			# maxF = 'No Data'
		# else:
			# # Get max
			# maxResult = max(result)
			# maxIndex = result.index(maxResult)
			# maxDate = date[maxIndex]
			# maxND = ND[maxIndex]
			# maxF = F[maxIndex]
		
			# # Write exceedances to outfile
			# if float(maxResult) > SLV:
				# foutExceedance.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')

			# # Check if active
			# if datetime.datetime(max(date).year, max(date).month, max(date).day) > datetime.datetime.strptime('2015-01-01', '%Y-%m-%d'):
				# foutActive.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\n')
			
		# # Write maxes to an outfile
		# fout.write(location+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')
		
		# Plot the data
		lns5 = ax1.plot_date([pd.to_datetime(start), pd.to_datetime(end)], [SLV, SLV], '-r', label = '7.48')
		lns1 = ax1.plot_date(date, result, '-', color='#00008B')
		lns2 = ax1.plot_date(date, result, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered')
		lns3 = ax1.plot_date(daysF, dataF, 'ob', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered')
		lns4 = ax1.plot_date(daysND, dataND, '.r', markersize=2, label = 'Non-Detect')
		
		# Compile labels
		lns = lns2+lns3+lns4+lns5
		labs = [l.get_label() for l in lns]
		
		# Plot the legend
		fig.legend(lns, labs, loc='upper right', fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)

		# if inpst in figureDict:
		ax1.set_title(location, loc='left', fontsize=12)
			
		# Set a grid on plot
		ax1.grid(True)

		# Make y axis labels
		ax1.set_ylabel('Chromium [$\mu$g/L]', color='k')
		# Limit axis
		pylab.ylim(0.1,1200)         # to control primary y-axis range
		# Make log scale
		ax1.set_yscale('log')
		# Control grid lines
		grid(b=True, which='major', color='k', linestyle='-')
		grid(b=True, which='minor', color='grey', linestyle='-', linewidth=0.25)
		
		ax1.xaxis.label.set_color('k')
		ax1.tick_params(axis='y', colors='k')
		ax1.yaxis.set_major_formatter(ScalarFormatter())

		# Rotate x axis labels
		plt.setp( ax1.xaxis.get_majorticklabels(), rotation=35 )
		# Raise up bottom and side to accomodate labels and legend
		plt.subplots_adjust(top=.88, bottom=.2, right=.95)

		# Adjust figure size
		fig.set_size_inches(7,5)
		fig.subplots_adjust(hspace=.3)
		
		# Check that destination directories exist and create if not
		if not os.path.exists(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Figures'+os.sep+input+os.sep):
			os.makedirs(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Figures'+os.sep+input+os.sep)

		# Save the figure
		fig.savefig(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Figures'+os.sep+input+os.sep+str(figureNumber)+'- '+location+'.png',dpi=500)
		figureNumber += 1
		
		# plt.show()
		plt.close('all')
		
	# fout.close()
	# foutExceedance.close()
	# foutActive.close()