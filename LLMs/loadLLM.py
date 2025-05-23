import accelerate, peft, bitsandbytes, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def loadLLM(llm=None):

	model=None
	tokenizer=None
	
	if llm is not None:
		try:
			device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
			if device==torch.device("cuda") :
				quantization_config = BitsAndBytesConfig(load_in_4bit=True,
					bnb_4bit_compute_dtype=torch.bfloat16,
					bnb_4bit_use_double_quant=True,
					bnb_4bit_quant_type= "nf4"
					)
				model = AutoModelForCausalLM.from_pretrained(llm,
					torch_dtype="auto",
					device_map="auto",
					quantization_config=quantization_config
					)
			else:
				model = AutoModelForCausalLM.from_pretrained(llm)
			
			tokenizer = AutoTokenizer.from_pretrained(llm)
		except:
			model=None
			tokenizer=None
	
	return (model, tokenizer)
