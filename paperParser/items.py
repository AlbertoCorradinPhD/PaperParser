# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class PaperparserItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()	
	title = Field()
	abstract = Field()
	authors = Field()
	firstAuthor= Field()
	PMID=Field()
	ID=Field()
	mainText= Field()
	mainText_exNLP= Field()
	journal=Field()
	year=Field()
	mainText_abNLP=Field()
	

	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()
	dirOfAbstracts=Field()
	dirOfMainTexts=Field()
	dirOfSummaries=Field()
	termOfSearch=Field()
