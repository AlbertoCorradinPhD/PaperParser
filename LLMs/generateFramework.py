
from printFiles import printTXT

def generateFramework(client, AI_input, resultsDir, output_filename):
	
	system_message = """
		You are an AI assistant that helps human by generating scientific reviews based on multiple summaries of original scientific articles.
		So you will be provided with a text that contains these summaries of scientific papers with their authors and titles.
		You should identify in the given text the summaries, the authors and the titles of these scientific articles.
		Then, write a scientific review based the provided text.
		The scientific review you will generate shall be as long as possible.
		Keep track of the references.

		Text:
		"""
	
	#select openAI model
	model="gpt-4o-mini" #funzione meglio di gpt-4o
	
	response = client.chat.completions.create(
		model=model, # engine = "deployment_name".
		messages=[
			{"role": "system", "content": system_message},
			{"role": "user", "content": AI_input},
		],
		temperature=0.6,
		max_tokens=16384,
		top_p=0.8,
		frequency_penalty=0.6,
		presence_penalty=0.8
	)
	
	framework= response.choices[0].message.content
	printTXT(output_filename, outputDirPath=resultsDir, title='', text=framework)
	
	return framework
