# Bar&PiePlotter.py

# This plots some summary statistics for the Cr dataset

# Written by Casey Gierke of Lee Wilson & Associates
# on 5/29/2020

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import pandas as pd
import os
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

# Adjust size of output plots
font = {'family' : 'Times New Roman',
	'weight' : 'light',
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

# def DB_get(SQL):
	# db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
						  # "Server="+server+";"
						  # "Database=Chromium;"
						  # "Trusted_Connection=yes;")
	# db.autocommit = True

	# # Prepare a cursor object using cursor() method
	# cursor = db.cursor()
	# cursor.execute(SQL)
	# result = cursor.fetchall()
	# db.close()
	# return result

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

# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

colors = ["green", "lightskyblue", "green", "pink", "purple"]

# ------------------------------------------------------
# COMPUTATIONS
# ------------------------------------------------------

# # Define SLV value
# SLV = 7.48

# Query out data
sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, PARAMETER_CODE, DETECTED, FILTERED FROM Chromium_Flagged"
df = pd.read_sql(sql, sql_conn)

# # ------------------------------------------------------
# # Simple bar plot

# # #average of different measurements across species
# ave = df.groupby(['PARAMETER_CODE']).mean() 

# # #standard deviation represents the variance in the data
# sd = df.groupby(['PARAMETER_CODE']).std() 

# # #use sd as error bar
# my_plot = ave.plot(kind='bar', yerr=sd) 
# my_plot.set_ylabel("Average values")

# plt.show()

# ------------------------------------------------------

# Make bar plot showing detected and non-detected samples and grouping by parameter code
my_plot = sns.barplot(x="DETECTED", y="Data", hue="PARAMETER_CODE", palette=['g','b'], data=df, edgecolor='k');
my_plot.set_ylabel("Average Cr values [$\mu$g/L]")
my_plot.set_ylabel("Detected")
my_plot.set_title('Detected and non-detected samples grouped by parameter code')
# plt.show()

# Check that destination directories exist and create if not
if not os.path.exists(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep):
	os.makedirs(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep)

# Save the figure
plt.savefig(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep+'Bar- Detect- Paramenter.png',dpi=500)

# Close figure
plt.close('all')

# ------------------------------------------------------
# Do pie charts

# Cr vs Cr(VI)
plt.pie(df.groupby(['PARAMETER_CODE']).count()['Data'], labels=pd.Series(df['PARAMETER_CODE'].unique()), colors=colors, autopct='%1.0f%%', wedgeprops={"edgecolor":"k",'linewidth': 1})

# Adjust properties
plt.axis('equal')
plt.title('Data by parameter type\nof '+str(df.Data.count())+' total')
# plt.show()   
   
# Save the figure
plt.savefig(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep+'Pie- Cr vs. Cr(VI).png',dpi=500)

# Close figure
plt.close('all')

# ------------------------------------------------------

# Detect
plt.pie(df.groupby(['DETECTED']).count()['Data'], labels=pd.Series(df['DETECTED'].unique()), colors=colors, autopct='%1.0f%%', wedgeprops={"edgecolor":"k",'linewidth': 1})

# Adjust properties
plt.axis('equal')
plt.title('Data by detect\nof '+str(df.Data.count())+' total')
# plt.show()   
   
# Save the figure
plt.savefig(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep+'Pie- Detect.png',dpi=500)

# Close figure
plt.close('all')

# ------------------------------------------------------

# Detect
plt.pie(df.groupby(['FILTERED']).count()['Data'], labels=pd.Series(df['FILTERED'].unique()), colors=colors, autopct='%1.0f%%', wedgeprops={"edgecolor":"k",'linewidth': 1})

# Adjust properties
plt.axis('equal')
plt.title('Data by filtered\nof '+str(df.Data.count())+' total')
# plt.show()   
   
# Save the figure
plt.savefig(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Stats'+os.sep+'Pie- Filter.png',dpi=500)

# Close figure
plt.close('all')
