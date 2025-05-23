
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate

from printFiles import printTXT
from buildRetriever import (getRetriever, format_docs)
from selectTools import (selectModel, selectREPLagent)
from manageParagraphs import (identifyParagraphs, retrieveParagraphContent)

import os
import requests

def humanize(examples, drafts_merged, system_content, user_instructions, resultsDir, api_key, organization, email=None, pwd=None):
	
	#RAG APPLICATION
	if examples is None:
		retriever= None
	else:
		print("\n\nRAG application to identify a writing style:")
		retriever=getRetriever(file_path=None, text=examples)
	
	
	#REPL APPLICATION
	print("\n\nREPL application to separate the paragraphs to rephrase:")
	paragraphs=identifyParagraphs(drafts_merged, api_key=api_key, organization = organization)
	#paragraphs_to_humanize=paragraphs[1:len(paragraphs)-1]
	print("\n\nThe paragraphs to humanize are the following:")
	print(paragraphs[1:len(paragraphs)-1])
	M=len(paragraphs)
	humanized_list=[paragraphs[0]] #initial step
	
	#define the model for rewriting text
	#model="gpt-4.5-preview"
	model="o3-mini-2025-01-31" 
	#model="gpt-4.1-2025-04-14"
	llm=selectModel(model, api_key=api_key, organization  = organization)

	#set new output directory
	outputDirPath = os.path.join(resultsDir, "paragraphsHumanized")
	os.makedirs(outputDirPath, exist_ok=True)
	print("\n\nOutput directory will be the following:")
	print(outputDirPath)
	
	#print the main title
	j=0
	title= paragraphs[j]
	output_filename= str(0)+str(j+1)+".txt"
	printTXT(output_filename,outputDirPath, title=title, text='')	
	
	for j in range(1, M, 1):	
		
		title= paragraphs[j]
		print('\n\nParagraph under consideration:')
		print(title)
		humanized_list.append("\n\n"+title)
		print('\nProceeding to retrieve it by REPL')
		paragraph_content= retrieveParagraphContent(title, text= drafts_merged, api_key=api_key, organization=organization)
		# all the paragraphs except References
		if j< M-1:	
			print('\nProceeding to humanize the paragraph')				
			response= humanizeOp(system_content, user_instructions, paragraph_content, llm, retriever, email, pwd  )			
			humanized_list.append("\n"+response)				
			#write it down
			if (j+1)<10:
				output_filename= str(0)+str(j+1)+".txt"
			else:
				output_filename= str(j+1)+".txt"
			printTXT(output_filename,outputDirPath, title=title, text=response)	
			print('Paragraph was humanized')	
		#References		
		else: 
			humanized_list.append("\n"+str(paragraph_content))
			print('Done')
		
	
	humanized= "".join(str(element) for element in humanized_list)
	if email is None or pwd is None:
		name="humanized"
	else: 
		name="humanized_antiDetector"
	output_filename= name+".txt"
	printTXT(output_filename,resultsDir, title='', text=humanized)
	return humanized , outputDirPath

def humanizeOp(system_content, user_instructions, paragraph_content, llm, retriever, email=None, pwd=None ):
	
	#define the prompt
	user_content= paragraph_content +"\n\n"+ user_instructions
	#print(user_content)
	messages = [
		{"role": "system", "content": system_content},
		{"role": "user", "content": user_content}
	]
	
	prompt = ChatPromptTemplate.from_messages(messages)	
	rag_chain= prompt | llm | StrOutputParser()
	if retriever is None:
		response = rag_chain.invoke({"examples": 'No example provide. Pass to next step.'})
	else:
		response =rag_chain.invoke({"examples": retriever | format_docs})
	if email is None or pwd is None:
		return response
	response = callHumanizingApp(text=response, email=email, pwd=pwd)		
	return response

def callHumanizingApp(text, email, pwd):
	"""
	Potential call to an anti-Ai detector app. To be complete
	"""
	email = email  # TODO: enter account email here
	password = pwd  # TODO: enter account password here
	text = text  # TODO: place your input text here

	return text
	 
	
	
