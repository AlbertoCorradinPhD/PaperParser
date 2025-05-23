import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface.llms import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate
from buildRetriever import format_docs
from getTexts import (read_content, get_mod_time, merge_per_folder)
from printFiles import printTXT


def generateAbstract(framework, paragraphs, outputDirPath, retriever, llm):
	
	# model="gpt-4o"
		
	template = """You are an AI assistant that helps human to generate scientific reviews.
		Based only on the following context: {context}, you should generate an abstract
		for the following short draft of scientific review:\n\n""" + framework
	#print(template)
	prompt = ChatPromptTemplate.from_template(template)
	rag_chain= prompt | llm | StrOutputParser()
	
	j=0
	paragraph=paragraphs[j].strip()
	#print(str(paragraph))
	response =rag_chain.invoke({"context": retriever | format_docs, "paragraph": paragraph})
	#print(response)
	output_filename= str(0)+str(j+1)+".txt"
	printTXT(output_filename, outputDirPath, title=paragraph, text=response)
	return response

	
def extendParagraphs(framework, paragraphs, outputDirPath, resultsDir, retriever, llm, filename): 
	
	# model="gpt-4o"	
		
	template = """You are an AI assistant that helps human to generate scientific reviews.
		Based only on the following context: {context}, you should extend as long as possible
		the paragraph entitled: {paragraph} of the following short draft of a scientific
		review: {framework}.\n\nPlease, keep track on the text of the references 
		indicated in the short draft while extending paragraphs but don't copy-and-paste 
		chapter "References" while extending the required paragraph.
		"""
	#print(template)
	prompt = ChatPromptTemplate.from_template(template)
	rag_chain= prompt | llm | StrOutputParser()
	
	L =len(paragraphs)
	for j in range(1, L-1, 1):
		paragraph=paragraphs[j].strip()
		print(str(paragraph))
		response =rag_chain.invoke({"context": retriever | format_docs, 
			"paragraph": paragraph, "framework": framework})
		if (j+1)<10:
			output_filename= str(0)+str(j+1)+".txt"
		else:
			output_filename= str(j+1)+".txt"			
		printTXT(output_filename, outputDirPath, title='', text=response)
			
	#merge generated paragraphs
	mergedParagraphs = merge_per_folder(outputDirPath)
	output_filename=filename+".txt"
	printTXT(output_filename, resultsDir, title='', text=mergedParagraphs)
	return mergedParagraphs, L 

def addReferences(mergedParagraphs, L, framework, outputDirPath, resultsDir, retriever, llm, filename):
	
	# model="gpt-4o-mini"
		
	template = """You are an AI assistant that helps human to generate scientific reviews.
		Write paragraph 'References' for the following text: \n\n"""+ mergedParagraphs+ """
		on the basis of the following context: {context}, and of the short draft it was extended from: 
		{framework}. \n\n Please, add as many references as possible.
		"""
	#print(template)
	prompt = ChatPromptTemplate.from_template(template)
	rag_chain= prompt | llm | StrOutputParser()
	response =rag_chain.invoke({"context": retriever | format_docs, "framework": framework})
	#print(response)
	j=L-1
	if j<10:
		output_filename= str(0)+str(j+1)+".txt"
	else:
		output_filename= str(j+1)+".txt"
	printTXT(output_filename, outputDirPath, title='', text=response)
		
	#write down the result	
	draft = merge_per_folder(outputDirPath) 
	output_filename= filename+".txt"
	printTXT(output_filename, resultsDir, title='', text=draft)
	return draft


		
		
		
