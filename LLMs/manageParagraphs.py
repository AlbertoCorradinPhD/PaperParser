from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from langchain.agents.agent_types import AgentType
from selectTools import (selectModel, selectREPLagent)
from logging import warning


def identifyParagraphs(framework, api_key, organization=None):
	
	#model="gpt-4o-mini"
	model="gpt-4.1-2025-04-14"
	llm=selectModel(model, api_key=api_key, organization  = organization)
	agent_executor = selectREPLagent(llm)

	#print(agent_executor.agent.llm_chain.prompt.template)
	
	query = """You are an AI assistant that helps human to interprete texts.
		You will be provided with a text (a draft of a scientific review)
		composed of several paragraphs. You should identify the main title of these
		scientific review and the titles of its paragraphs.
		Then return these titles as a Python list object. Include in your answer the
		paragraph 'References' if present in the following draft:
		Draft:
		""" + framework

	paragraphs= None	

	while paragraphs is None:
		try:
			paragraphs= agent_executor.run(query)
		except Warning:
			paragraphs=None
		except:
			paragraphs=None
		if paragraphs is not None:
			K=paragraphs.find('Agent stopped')
			if K>=0:
				paragraphs=None
	
	#print(paragraphs)
	#print(type(paragraphs))
	
	# parsing and casting  of the response
	temp = paragraphs.replace("[", "")
	temp = temp.replace("]", "")
	temp = temp.replace("'", "") 
	temp = temp.replace("```", "")
	temp = temp.replace('"','')
	temp = temp.replace('python','')
	temp = temp.replace('\n','')
	temp=temp.split(",")
	strip_list = []
	for x in temp:
		strip_list.append(x.strip())
	
	paragraphs=strip_list	
	return paragraphs
	
def retrieveParagraphContent(title, text, api_key, organization=None):
	
	#model="gpt-4o-mini"
	model="gpt-4.1-2025-04-14"
	llm=selectModel(model, api_key=api_key, organization  = organization)
	agent_executor = selectREPLagent(llm)

	#print(agent_executor.agent.llm_chain.prompt.template)	
	
	query = """You are an AI assistant that helps human to interprete texts.
		You will be provided with a scientific review and a paragraph title:
		""" + title +""".\nYou should identify this paragraph in the 
		given scientific review and return its content as a string. 
		Scientific review:""" + text
	
	paragraph_content=None
	while paragraph_content is None:
		try:
			paragraph_content= agent_executor.run(query)
		except Warning:
			paragraph_content=None
		except:
			paragraph_content=None
		if paragraph_content is not None:
			K=paragraph_content.find('Agent stopped')
			if K>=0:
				paragraph_content=None
		
	return paragraph_content

