import datetime
import socket
import scrapy


from urllib.parse import urlparse, urljoin
from scrapy.http import Request
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, Join


from paperParser.items import PaperparserItem

# for init and parse files
import re
import time
import os

#for R packages management
#import rpy2

#additional
import random

class BasicSpider(scrapy.Spider):
	name = "rev9" 
	pubmedUrl="https://pubmed.ncbi.nlm.nih.gov/"
	allowed_domains=[]
	allowed_domains.append(urlparse(pubmedUrl).netloc)
 
	
	def __init__(self, term=None, *args, **kwargs):
		super(BasicSpider, self).__init__(*args, **kwargs)		
		self.start_urls = []
		self.term= term		
		self.start_urls.append(self.pubmedUrl+ ("?term=%s" % self.term))
		cwd=os.getcwd()
		self.dirOfAbstracts = os.path.join(cwd, "abstracts") 
		os.makedirs(self.dirOfAbstracts, exist_ok=True)
		self.dirOfMainTexts = os.path.join(cwd, "mainTexts") 
		os.makedirs(self.dirOfMainTexts, exist_ok=True)
		self.dirOfSummaries = os.path.join(cwd, "articlesSummaries") 
		os.makedirs(self.dirOfSummaries, exist_ok=True)
	
		
	def parse(self, response):
		
		user_agents_list = [ #fake user agent
			'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
			]
				
		# Ricerca orizzontale
		print('20 secs of pause')
		time.sleep(20)
		next_selector = response.xpath('//*[contains(@class,"search-results-chunk results-chunk")]//@data-next-page-url')
		for data in next_selector.extract():						
			url= re.sub(pattern='/more/', repl='', string=data)
			yield Request(urljoin(self.pubmedUrl, url), headers={'User-Agent':random.choice(user_agents_list)})
		
		# Ricerca verticale
		print('20 secs of pause')
		time.sleep(20)
		item_selector = response.xpath('//*[contains(@class,"docsum-wrap")]//@href')
		for url in item_selector.extract():
			yield Request(urljoin(self.pubmedUrl, url), callback=self.parse_item , headers={'User-Agent': random.choice(user_agents_list)})			
		

	def parse_item(self, response):  
		# Create the loader using the response
		l = ItemLoader(item=PaperparserItem(), response=response)
		
		# Housekeeping fields
		#NB: add_value crea degli oggetti list
		l.add_value('url', response.url)
		l.add_value('project', self.settings.get('BOT_NAME'))
		l.add_value('spider', self.name)
		l.add_value('server', socket.gethostname())
		l.add_value('date', datetime.datetime.now())
		l.add_value('dirOfAbstracts', self.dirOfAbstracts)
		l.add_value('dirOfMainTexts', self.dirOfMainTexts)
		l.add_value('dirOfSummaries', self.dirOfSummaries)
		l.add_value('termOfSearch', self.term)
		      
		# Load fields using XPath expressions
		
		title= ''.join(response.xpath('//*[contains(@name,"citation_title")]/@content').extract()[0]).strip()		
		l.add_value('title', title, MapCompose(lambda x:x.strip()))
		authors= ', '.join(response.xpath('//*[contains(@name,"citation_authors")]/@content').extract())
		l.add_value('authors', authors)
		try:
			journal= ', '.join(response.xpath('//*[contains(@name,"citation_journal_title")]/@content').extract())
		except:
			journal= ', '.join(response.xpath('//*[contains(@name,"citation_doi")]/@content').extract())
		l.add_value('journal', journal)
		year= ', '.join(response.xpath('//*[contains(@name,"citation_date")]/@content').extract())
		l.add_value('year', year)
		abstract= ''.join(response.xpath('//*[contains(@class,"abstract-content selected")]/p/text()').extract())
		abstract= re.sub(pattern='\n', repl='', string=abstract)
		rgx = re.compile("(\s\s+)")
		abstract= re.sub(pattern=rgx, repl='', string=abstract)
		l.add_value('abstract', abstract,MapCompose(lambda x:x.strip()))    
		temp=re.split("/", response.url)
		l.add_value('PMID', temp[len(temp)-2]) 
		
		 
		return l.load_item()
 
