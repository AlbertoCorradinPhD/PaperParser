

def parseXML(myItem, isBook=False):
	
	
	doc= None
	
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
		return doc
	
	if isBook:
		doc= europepmc.epmc_ftxt_book(myItem['ID'])
		#journal='Book'
		res= europepmc.epmc_search(query=myItem['title'][0])					
		# To pandas DataFrame
		with (ro.default_converter + pandas2ri.converter).context():
			pd_dt = ro.conversion.get_conversion().rpy2py(res)
		pd_dt= pd_dt[pd_dt["pmid"]==myItem["PMID"][0]]
		#year= str(pd_dt["pubYear"].iloc[0])
	else:
		doc = tidypmc.pmc_xml(myItem['ID'])		
	
	return doc
