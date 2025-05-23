import torch
import gc

def nlp_sciLit(text, model, tokenizer):
	
	prompt = "Can you summarize this article for me?\n" + text
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": prompt}
	]
	
	text = tokenizer.apply_chat_template(messages,
		tokenize=False,
		add_generation_prompt=True
	)
	
	#define the device
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	if device==torch.device("cuda"):
		gc.collect()
		torch.cuda.empty_cache()
	
	model_inputs = tokenizer([text], return_tensors="pt").to(device)
	generated_ids = model.generate(
		model_inputs.input_ids,
		max_new_tokens=1000,
		min_new_tokens=500,
		pad_token_id = tokenizer.eos_token_id,
		eos_token_id=model.config.eos_token_id,
		num_beams=4,
		early_stopping=True,
		repetition_penalty=1.4
	)
	generated_ids = [
		output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
	]
	response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
	return response
