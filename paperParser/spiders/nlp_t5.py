

def nlp_t5(text):
	import torch                
	from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
	
	tokenizer = AutoTokenizer.from_pretrained('t5-base')                        
	model = AutoModelForSeq2SeqLM.from_pretrained('t5-base', return_dict=True) 
	N= 1024
	
	# From here, you can use any data you like to summarize. Once you have 
	# gathered your data, input the code below to tokenize it:
	inputs = tokenizer.encode("summarize: " + text,                  
		return_tensors='pt', max_length=N,truncation=True)  
	
	#Now, you can generate the summary by using the model.generate function on T5:
	summary_ids = model.generate(inputs, max_new_tokens=N,# max_length=150, min_length=80, 
		length_penalty=5., num_beams=2)
	
	#Feel free to replace the values mentioned above with your desired values. 
	#Once it’s ready, you can move on to decode the tokenized summary 
	# using the tokenizer.decode function:       
	summary = tokenizer.decode(summary_ids[0],skip_special_tokens=True)
	# And there you have it: a text summarizer with Google’s T5. You can 
	#replace the texts and values at any time to summarize various arrays of data
	return summary
