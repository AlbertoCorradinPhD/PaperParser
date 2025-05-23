import pandas as pd
import time

from paperParser.spiders.parseXML import parseXML

def getDocument(myItem, isBook=False):
	
	#default
	mainText= "Exception"
	myItem['mainText']= mainText
		
	
	print("ID under parsing:")
	print(myItem['ID'])
	
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
		return myItem
		
	#loop per affrontare problemi di connessione
	print("I try to get the document from the PubmedCentral")
	i=0
	doc=None
	while doc is None:			
		i=i+1			
		if i>10:
			print("Problems with the Internet connection")
			break
		try:
			doc = parseXML(myItem, isBook)		
		except:
			print('This was try number: '+str(i))
			time.sleep(3)				
	
	if doc is None:
		print('I cannot parse the XML document')
		return myItem		
	else:
		print('I got the XML document')
		txt= tidypmc.pmc_text(doc)	
		# To pandas DataFrame
		with (ro.default_converter + pandas2ri.converter).context():
			pd_dt = ro.conversion.get_conversion().rpy2py(txt)		
		#print(pd_dt)
		
		if isinstance(pd_dt, pd.DataFrame):
			print("R dataframe of main text was converted to pandas dataframe")
			toAvoid=["Title","TITLE","Abstract","ABSTRACT","Methods", 
				"METHODS","Materials and Methods", "MATERIALS AND METHODS",
				"Chapter Notes; Author History", "CHAPTER NOTES; AUTHOR HISTORY"]
			boolean=pd_dt["section"].apply(lambda x: x not in toAvoid )
			pd_mainText= pd_dt.loc[boolean , "text"]
			mainText = ' '.join(pd_mainText)
			print("...got main text")
			myItem['mainText']= mainText

		else: 
			print("It was not possible to convert the XML document into pandas dataframe")	
		return myItem
