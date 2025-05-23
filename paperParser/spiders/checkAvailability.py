
import pandas as pd
import time
import re

def checkAvailability(myItem):
	
	#default
	isOpenAccess= False
	isBook= False 
	isEPMC= False
	
	
	print("Title under search:")
	print(myItem['title'][0])
	
	try:
		import rpy2
		import rpy2.robjects as ro
		from rpy2.robjects.packages import importr
		from rpy2.robjects import pandas2ri
		utils = importr('utils')
		base = importr('base')
		tidyverse = importr('tidyverse')
		tidypmc = importr('tidypmc')		
		xml2 = importr('xml2')
		europepmc = importr('europepmc')
	except:
		print('I cannot import R objects')	
		return isOpenAccess, isBook, isEPMC
	
	#loop per affrontare problemi di connessione
	print("Attempt to connect to database 'europepmc' ")
	i=0
	res=None
	while res is None:
		i=i+1
		if i>10:
			print("Problems with the Internet connection")				
			break
		try:
			res = europepmc.epmc_search(query=myItem['PMID'][0])
			
		except:	
			print('This was try number: '+str(i))
			time.sleep(3)
	
	if res is None:
		print('I cannot get this title from "europepmc" database')
		return isOpenAccess, isBook, isEPMC
	else:
		print('I found this title')
		# To pandas DataFrame
		with (ro.default_converter + pandas2ri.converter).context():
			pd_dt = ro.conversion.get_conversion().rpy2py(res)
		print("R dataframe of search's results was converted to pandas dataframe")
		#PMID= myItem["PMID"][0]
		#print("test PMID")
		#print(PMID)
		pd_dt= pd_dt[pd_dt["pmid"]== myItem["PMID"][0]]
		isOpenAccess= pd_dt["isOpenAccess"].iloc[0]=='Y'
		isBook= bool(re.search("book", pd_dt["pubType"].iloc[0]))		
		isEPMC= pd_dt["inEPMC"].iloc[0]=='Y'
		return isOpenAccess, isBook, isEPMC

