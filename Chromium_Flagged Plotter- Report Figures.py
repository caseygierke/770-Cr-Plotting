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
inputPath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Tables'+os.sep

# Get all the files to plot
files = []
for file in glob.glob(inputPath+"*.txt"):
    files.append(file)

# # Short Circuit
# # Alluvial
# files = [files[2]]
# Alluvial appendix
files = [files[0]]
# # Regional
# files = [files[-7]]

# Loop through files for plotting different parts
for file in files:

	# Make dictionary for appendix figures
	figureDict = {}
	Dictin = open(file,'r')

	# Get input from file
	input = file[find_last(file,os.sep)+1:-4]
	
	# Read in data
	for line in Dictin:
		columns = line.split('\t')
		figureDict[columns[0]] = {'Lat': columns[2], 'Long': columns[3], 'Aquifer': columns[1]}
		
	# # Short circuit
	# figureDict = {'SWA-4-12': figureDict['SWA-4-12'],
					# 'MCO-0.6': figureDict['MCO-0.6']
					# }

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

		# print('Working on '+location)

		# Open figure for plotting
		fig = plt.figure()
		
		# Define axis for plotting
		ax1 = fig.add_subplot(111)

		# ------------------------------------------------------
		# Query out Cr data
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
			
			# # Check for ND = 10 condition
			# if row[2] == 'N' and float(row[1]) == 10.0:
				# continue

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
		# Query out hex data
		sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND PARAMETER_CODE = 'Cr(VI)' ORDER BY SAMPLE_DATE"
		dataHex = DB_get(sql)
			
		# Initialize arrays
		dateHex = []
		resultHex = []
		NDHex = []
		FHex = []
		daysNDHex = []
		dataNDHex = []
		daysFHex = []
		dataFHex = []

		# Loop through data
		for row in dataHex:
			
			# Check for ND = 10 condition
			if row[2] == 'N' and float(row[1]) == 10.0:
				continue

			# Append values
			dateHex.append(row[0])
			resultHex.append(float(row[1]))
			NDHex.append(row[2])
			FHex.append(row[3])
			
			# Check for non-detects
			if row[2] == 'N':
				daysNDHex.append(row[0])
				dataNDHex.append(float(row[1]))
			# Check for filtering
			if row[3] == 'Y':
				daysFHex.append(row[0])
				dataFHex.append(float(row[1]))
		
		# ------------------------------------------------------
		# OUTPUTS
		# ------------------------------------------------------
		
		# Determine which kind of plot to produce
		
		# Check if there is not data
		if result == [] and resultHex == []:
			print(location+' has no data, moving on.')
			continue

		# Check if there is only Cr data
		elif result != [] and resultHex == []:
			print(location+' has Cr data but no Cr(VI) data. Plot only Cr.')
		
			# Plot the data
			lns5 = ax1.plot_date([pd.to_datetime(start), pd.to_datetime(end)], [SLV, SLV], '-r', label = '7.48')
			# lns1 = ax1.plot_date(date, result, '-', color='#00008B')
			lns2 = ax1.plot_date(date, result, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered Cr')
			lns3 = ax1.plot_date(daysF, dataF, 'ob', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered Cr')
			lns4 = ax1.plot_date(daysND, dataND, '.r', markersize=2, label = 'Non-Detect')
			
			# Compile labels
			lns = lns2+lns3+lns4+lns5
			labs = [l.get_label() for l in lns]
			
			# Plot the legend
			# fig.legend(lns, labs, loc='upper left', fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)
			fig.legend(lns, labs, bbox_to_anchor=(0.31,1.0), bbox_transform=plt.gcf().transFigure, fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)

		# Check if there is only Cr(VI) data
		elif result == [] and resultHex != []:
			print(location+' has no Cr data but does have Cr(VI) data. Plot only Cr(VI).')
		
		# Check if there is only Cr(VI) data
		elif result != [] and resultHex != []:
			print(location+' has Cr and Cr(VI) data. Plot both.')
		
			# Plot the Cr data
			lns5 = ax1.plot_date([pd.to_datetime(start), pd.to_datetime(end)], [SLV, SLV], '-r', label = '7.48')
			# lns1 = ax1.plot_date(date, result, '-', color='#00008B', label = 'Cr')
			lns2 = ax1.plot_date(date, result, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered Cr')
			lns3 = ax1.plot_date(daysF, dataF, 'ob', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered Cr')
			lns4 = ax1.plot_date(daysND, dataND, '.r', markersize=2, label = 'Non-Detect')
			
			# Plot the Cr data
			# lns6 = ax1.plot_date(dateHex, resultHex, '-.', color='c', label = 'Cr(VI)')
			lns7 = ax1.plot_date(dateHex, resultHex, '^', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered Cr(VI)')
			lns8 = ax1.plot_date(daysFHex, dataFHex, '^b', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered Cr(VI)')
			lns9 = ax1.plot_date(daysNDHex, dataNDHex, '.r', markersize=2, label = 'Non-Detect')
			
			# Compile labels
			lns = lns2+lns3+lns7+lns8+lns4+lns5
			labs = [l.get_label() for l in lns]
			
			# Plot the legend
			# fig.legend(lns, labs, loc='upper left', fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)
			fig.legend(lns, labs, bbox_to_anchor=(0.34,1.0), bbox_transform=plt.gcf().transFigure, fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)

		# else:
			# print("I don't know what happened!")
				
		# # Plot the data
		# lns5 = ax1.plot_date([pd.to_datetime(start), pd.to_datetime(end)], [SLV, SLV], '-r', label = '7.48')
		# lns1 = ax1.plot_date(date, result, '-', color='#00008B')
		# lns2 = ax1.plot_date(date, result, 'o', color='#B0E2FF', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Unfiltered')
		# lns3 = ax1.plot_date(daysF, dataF, 'ob', markersize=3.5, markeredgecolor='k', markeredgewidth='0.5', label = 'Filtered')
		# lns4 = ax1.plot_date(daysND, dataND, '.r', markersize=2, label = 'Non-Detect')
		
		# # Compile labels
		# lns = lns2+lns3+lns4+lns5
		# labs = [l.get_label() for l in lns]
		
		# # Plot the legend
		# fig.legend(lns, labs, loc='upper right', fontsize= 9, prop={'size':9}, numpoints=1, framealpha=1)

		# if inpst in figureDict:
		ax1.set_title(location, loc='right', fontsize=12)
			
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
		
