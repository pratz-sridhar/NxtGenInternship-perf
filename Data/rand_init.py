import numpy as np
import math
import pandas as pd

zones = ['AMD.csv','BLR.csv','FDB.csv','MUM.csv'];

for zone in zones:
	df = pd.read_csv(zone);
	n = np.shape(df)[0];
	rand1 = np.random.normal(loc=50.0,scale=30.0,size=n);
	rand2 = np.random.normal(loc=50.0,scale=30.0,size=n);
	for k in range(0,n):
		r = math.floor(rand1[k]);
		j = math.floor(rand2[k]);
		if(r<2):
			r=5;
		if(r>98):
			r=98;
		df.set_value(k,"CPU_UTIL",r);
		if(j<2):
			j=5;
		if(j>98):
			j=98;
		df.set_value(k,"MEM_UTIL",j);
		df.to_csv(zone,index=False);