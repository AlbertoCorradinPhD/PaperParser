
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface.llms import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate
from printFiles import printTXT
from selectTools import selectModel

def merge2Drafts(drafts,resultsDir, api_key, organization):
	
	#generate the draft
	print("\n\nI am going to merge the drafts in input:")
	model="o1-mini-2024-09-12"
	llm=selectModel(model, api_key=api_key, organization  = organization)
	drafts_merged=mergingOp(drafts[0],drafts[1], resultsDir, llm)
	name="drafts_merged"
	output_filename= name+".txt"
	printTXT(output_filename, outputDirPath=resultsDir, title='', text=drafts_merged)
	print("\nDrafts were merged.")
	return drafts_merged

def mergingOp(draft_direct, draft_reverse, resultsDir, llm):
	
	
	template = """You are an AI assistant that helps human to generate scientific reviews.
		You will be given two distinct reviews on the same subject and you will merge
		them in a unique text. Keep track of the references while merging the reviews, 
		and list all of them at the end in a unique paragraph entitled 'References'.
		Review number 1: {draft_direct}, review number 2: {draft_reverse}.
		Do not to lose information: the text you are going to create should be as 
		long as possible. 
		"""
	#print(template)
	prompt = ChatPromptTemplate.from_template(template)
	rag_chain= prompt | llm | StrOutputParser()
	
	response =rag_chain.invoke({"draft_direct": draft_direct, "draft_reverse": draft_reverse})	
	return response
