
from generateExtensions import (generateAbstract, extendParagraphs, addReferences)
from manageParagraphs import identifyParagraphs
from buildRetriever import getRetriever
from selectTools import selectModel
import os


def elongateFrameworks(frameworks, resultsDir, AI_inputs, suffixes, api_key, organization):	
	
	M=len(frameworks)
	drafts=[]
	
	for i in range(M):		
		
		framework= frameworks[i]
		AI_input= AI_inputs[i]
		
		#REPL APPLICATION
		print("\n\nREPL application to identify the paragraphs to extend:")
		paragraphs=identifyParagraphs(framework, api_key=api_key, organization = organization)
		print("\n\nIdentified paragraphs are the following:")
		print(paragraphs)
		#print(type(paragraphs))
		
		#RAG APPLICATION
		print("\n\nRAG application to create a context:")
		retriever=getRetriever(file_path=None, text=AI_input)
		
		#set new output directory
		outputDirPath = os.path.join(resultsDir, "paragraphsExtensions"+suffixes[i])
		os.makedirs(outputDirPath, exist_ok=True)
		print("\n\nOutput directory will be the following:")
		print(outputDirPath)
		
		#GENERATE THE DRAFT
		print("\n\nGeneration of the draft:")
		model="gpt-4o"
		llm=selectModel(model, api_key=api_key, organization  = organization)
		
		#generate the abstract after the title
		abstract= generateAbstract(framework, paragraphs, outputDirPath, retriever, llm)
		print("\n")
		print(abstract)		
		
		#extend paragraphs
		print("\n\nThe following paragraphs will be extended:")
		print("\n")
		name="mergedParagraphs"+suffixes[i]
		mergedParagraphs, L = extendParagraphs(framework, paragraphs, outputDirPath, resultsDir, retriever, llm, filename=name)
		name="draft"+suffixes[i]
		draft= addReferences(mergedParagraphs, L, framework, outputDirPath, resultsDir, retriever, llm, filename=name)
		print("\n\nDraft has been generated and stored in the results' directory:")
		print(resultsDir)
		drafts.append(draft)
		
	return drafts
		
