from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.text import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema.document import Document
#from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline

def getRetriever(file_path=None, text=None):
	
	if file_path is None:
		all_splits = get_text_chunks_from_str(text)		
	else:
		loader = TextLoader(file_path=file_path)
		documents = loader.load()
		text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
		all_splits = text_splitter.split_documents(documents)
	#print(type(all_splits))
	#print(type(all_splits[0]))
	#print(all_splits[2].page_content)
	vectorstore = FAISS.from_documents(all_splits, HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
	retriever = vectorstore.as_retriever()
	return retriever

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)


def get_text_chunks_from_str(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return all_splits


