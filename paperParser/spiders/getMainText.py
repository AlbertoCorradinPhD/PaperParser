# Load Packages 
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re


#call spiders methods
from paperParser.spiders.checkAvailability import checkAvailability
from paperParser.spiders.getDocument import getDocument
	
	
def getMainText(myItem):
	# Investigate the availability of the article
	#default

	#investigate web page with the abstract only
	webpage = requests.get(myItem['url'][0]) 
	soup = BeautifulSoup(webpage.content, "html.parser") 
	dom = etree.HTML(str(soup)) 		
	#questi invece sono gli url dei full text
	hrefs=set(dom.xpath('//*[contains(@class,"full-text-links-list")]//@href')) 
	
	for href in hrefs:

		if bool(re.search("pmc", href)):
			print("Research article available in PMC")
			href=set(dom.xpath('//*[contains(@class,"identifier pmc")]//@href')) 
			temp=re.split("/", list(href)[0])
			myItem['ID']=temp[len(temp)-2]
			myItem= getDocument(myItem, isBook=False)			
			break
		else:
			print("No research article available in PMC. I search elsewhere")			
			isOpenAccess, isBook, isEPMC = checkAvailability(myItem)
			if isOpenAccess:
				print("Publication is open access. Then I try to retrieve it")
				if isBook:	
					print("This is a book")
					temp=re.split("/", href)
					myItem['ID']=temp[len(temp)-1]	
					myItem= getDocument(myItem, isBook=True)
					break
			else:
				myItem['mainText']= 'No free article'
	return myItem
