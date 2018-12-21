import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime as dt
from datetime import timedelta

def search(servername,d):
	""" This function returns server uptime, cpu utilization and memory utilization for a supplied servername. 
	If more than one instances of servername exists, returns -1,-1,-1. """
	zone = servername[0:3];
	zone+=".csv";
	zone = "Data/"+zone;
	df = pd.read_csv(zone);
	df.set_index("HOSTNAME" ,inplace = True);
	d1 = df.loc[servername];
	n = np.shape(d1)[0];
	m=np.shape(np.shape(d1))[0];
	t =d1.duplicated('Week',keep='first')
	flag =0
	for a in t:
		if(a==True):
			flag = 1
	if (n>1 and m>1 and flag==1):
		return -1,-1,-1;
	elif(m==1 or (n>1 and m>1 and flag==0)):
		dates = d1['Week'].unique().tolist()
		date_sameweek = check_week(dates , d)
		dd1 = d1.loc[d1.Week == date_sameweek]
		up = dd1["UPTIME"][0];
		cpu = dd1["CPU_UTIL"][0];
		mem = dd1["MEM_UTIL"][0];
		labels = 'Memory Utilized','Memory Free';
		size = [mem,100-mem];
		explode = (0,0.1);
		if(mem<75):
			colors="g","b";
		elif(mem>=75 and mem<90):
			colors="y","b";
		elif(mem>=90):
			colors="r","b";
		plt.figure(1);
		plt.subplot(121);#subplot declaration No.1
		plt.pie(size,explode,labels,colors, autopct="%1.0f",shadow=True, startangle=90, labeldistance = 1);
		plt.legend();
		plt.axis('equal');
		labels='CPU Utilized','CPU Free';
		size=[cpu,100-cpu];
		if(cpu<75):
			colors="g","b";
		elif(cpu>=75 and mem<90):
			colors="y","b";
		elif(cpu>=90):
			colors="r","b";
		plt.subplot(122);#subplot declaration No.2
		plt.pie(size,explode,labels,colors, autopct="%1.0f",shadow=True, startangle=90, labeldistance = 1);
		plt.axis('equal');
		script_dir = os.path.dirname(__file__)
		results_dir = os.path.join(script_dir, 'images/')
		file_name = "s1.png"
		if not os.path.isdir(results_dir):
			os.makedirs(results_dir)
		plt.legend();
		strFile = results_dir + file_name
		if os.path.isfile(strFile):
			os.remove(strFile)
		plt.savefig(strFile);
		plt.close();
		return up, cpu, mem;

def update(zone,param,d):
	pass
	"""parameters : zone is str like BLR and data id is int like 0,1,2.
	0 means uptime, 1 means cpu util and 2 means mem util. use the 2 parameters to update image.
	eg, zone = FDB, dataid = 1.Update FDB1.png with cpu util data for all servers from faridabad. 
	Also set or show threshold and point to data beyond threshold."""
	file_name = zone +str(param)+".png"
	zone+=".csv";
	zone = "Data/"+zone;
	df1 = pd.read_csv(zone);
	dates = df1['Week'].unique().tolist()
	date_sameweek = check_week(dates , d)
	df = df1.loc[df1.Week == date_sameweek]
	if (param==0):
		data = df['UPTIME']
	if(param==1):
		data = df['CPU_UTIL']
	if(param==2):
		data = df['MEM_UTIL']
	labels = df['HOSTNAME']
	n=np.shape(data)[0]
	x=np.arange(n)
	plt.bar(x,data)
	plt.xticks(x,labels, rotation = 'vertical')
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.4)
	script_dir = os.path.dirname(__file__)
	results_dir = os.path.join(script_dir, 'images/')
	if not os.path.isdir(results_dir):
		os.makedirs(results_dir)
	plt.legend();
	strFile = results_dir + file_name
	if os.path.isfile(strFile):
		os.remove(strFile)
	plt.savefig(strFile);
	plt.close();

def check_week(dates , date_in):
	d_in = dt.strptime(date_in, "%Y-%m-%d")
	days2 = dt.weekday(d_in)
	d_in1 = d_in - timedelta(days=days2)
	for d in dates :
		d_1 = dt.strptime(d,"%d-%m-%Y")
		days1 = d_1.weekday()
		d_2 = d_1 - timedelta(days=days1)
		if(d_2 == d_in1):
			return d