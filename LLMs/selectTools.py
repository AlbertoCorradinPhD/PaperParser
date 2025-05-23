from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from langchain.agents.agent_types import AgentType

def selectModel(model, api_key, organization=None):
	
	if model in ["gpt-4o", "gpt-4o-mini"]: 
		max_tokens=16384
		llm = ChatOpenAI(model=model, 
			temperature=0.8,
			max_tokens=max_tokens,
			top_p=0.8,
			api_key= api_key,
			organization=organization,
			)
	if model in ["o1-mini-2024-09-12"]: 
		max_tokens=65536
		llm = ChatOpenAI(model=model, 
			#temperature=0.6,
			max_tokens=max_tokens,
			#top_p=0.8,
			api_key= api_key,
			organization=organization,
			)
	if model in ["gpt-4.5-preview", "gpt-4.1", "gpt-4.1-2025-04-14"]: 
		max_tokens=16384
		llm = ChatOpenAI(model=model, 
			#temperature=0.6,
			max_tokens=max_tokens,
			#top_p=0.8,
			api_key= api_key,
			organization=organization,
			)
	if model in ["o3-mini","o3-mini-2025-01-31" ]: 
		max_completion_tokens =16384
		llm = ChatOpenAI(model=model, 
			#temperature=0.6,
			max_completion_tokens =max_completion_tokens ,
			#top_p=0.8,
			api_key= api_key,
			organization=organization,
			)
	if model in ["o3-2025-04-16"]: 
		max_completion_tokens =100000
		llm = ChatOpenAI(model=model, 
			#temperature=0.6,
			max_completion_tokens =max_completion_tokens,
			#top_p=0.8,
			api_key= api_key,
			organization=organization,
			)

	return llm

def selectREPLagent(llm):
	
	agent_executor = create_python_agent(
		llm=llm,
		tool=PythonREPLTool(),
		verbose=False,
		agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
		handle_parsing_errors=True
		)
		
	return agent_executor
