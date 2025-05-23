# Load Packages
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def nlp_textRank(text,SENTENCES_COUNT = 10):
	# Creating text parser using tokenization
	parser = PlaintextParser.from_string(text, Tokenizer("english"))
	
	# Summarize using sumy TextRank
	summarizer = TextRankSummarizer()
	summary = summarizer(parser.document,SENTENCES_COUNT)
	text_summary = ""
	for sentence in summary:		
		text_summary += str(sentence)
		text_summary += "\n\n"
	return text_summary
