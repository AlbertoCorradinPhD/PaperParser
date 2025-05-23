
import openai
from openai import OpenAI

def connectOpenAI(api_key, organization=None, project=None, model="gpt-4o-mini"):
		
	
	try:
		openai.api_key=api_key
		print(openai.chat.completions.create(
			model=model,
			messages=[{'role':'user','content': 'sup, bot?'}]
			).choices[0].message.content)
		
		client = OpenAI(
			api_key=  api_key,
			organization= organization,
			project= project
			)
		return client
	except:		
		print("connection failed")
		print(openai.api_key)
		return None
	
	
	
