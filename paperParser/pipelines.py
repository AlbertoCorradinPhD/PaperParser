# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from paperParser.items import PaperparserItem
import os
import re


# call spiders methods
from paperParser.spiders.getMainText import getMainText
from paperParser.spiders.nlp_textRank import nlp_textRank
from paperParser.spiders.storeSummaries import storeSummaries
from paperParser.spiders.storeSources import storeSources
from paperParser.spiders.nlp_t5 import nlp_t5 

#for t5
import torch                
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#for textRank
import nltk
nltk.download('punkt_tab')



class PaperparserPipeline (object):
	
	def process_item(self,myItem, spider):
		
		# INTRODUCTION
		print('This is pipeline in action:')		
		#get first author
		rgx = re.compile("(\w[\w']*\w|\w)")
		firstAuthor = rgx.findall(myItem['authors'][0])[0]
		#if len(firstAuthor) <3:
		#	firstAuthor = rgx.findall(myItem['authors'][0])[2]
		myItem['firstAuthor']=firstAuthor
		
		# ABSTRACT
		print('Store abstract')
		storeSources(myItem,firstAuthor, main=False)
		
		#GET FULL TEXT
		print('Full text searching...')
		myItem['mainText']="Exception" 
		myItem= getMainText(myItem)				
		#check
		boolean= myItem['mainText'] not in ["No free article","Exception"]
		
		# NLP FOR MAIN TEXT
		if boolean:
			print('Store main text')
			storeSources(myItem,firstAuthor, main=True)	
					
			#extractive NLP
			exNLP=nlp_textRank(text=myItem['mainText'])		
			myItem['mainText_exNLP']= exNLP				
			
			#abstractive NLP
			print("Abstractive NLP performed by Google T5 application")
			abNLP=nlp_t5(text=myItem['mainText'])
			myItem['mainText_abNLP']= abNLP
								
			storeSummaries(myItem, firstAuthor)
			print("Basic summaries of the main text was printed in pdf format")

		else:			
			print(myItem['mainText']) #stampa a schermo["No free article","Exception"]
		print('End of the pipeline' )
		return
