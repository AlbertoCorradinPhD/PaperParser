
from fpdf import FPDF
import os
import re

def storeSummaries(myItem,firstAuthor):
	# save FPDF() class into a variable pdf
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size = 10)
 
 	# add another cell
	text= myItem['title'][0].encode('utf-8').decode('latin-1')
	pdf.multi_cell(0, 5, txt = text)
			
	
	# create multicell
	text=myItem['authors'][0].encode('utf-8').decode('latin-1')
	pdf.multi_cell(0, 5, txt = text)
	pdf.cell(200, 15, txt = "", ln = 2, align = 'C')
	#report journal and year
	text='Journal: '+myItem['journal'][0].encode('utf-8').decode('latin-1')
	pdf.cell(80, 10, text, 0, 1, 'C')
	text='Year: '+myItem['year'][0].encode('utf-8').decode('latin-1')
	pdf.cell(20, 10, text, 0, 1, 'C')
	#testo rigenerato
	pdf.cell(200, 15, txt = "", ln = 2, align = 'C')
	pdf.cell(200, 15, txt = "Summary of main text"+" "+"(Abstractive Natural Language Processing)", ln = 2, align = 'C')
	#pdf.cell(200, 15, txt = "(Abstractive Natural Language Processing)", ln = 2, align = 'C')
	text= myItem['mainText_abNLP'].encode('utf-8').decode('latin-1') 	
	pdf.multi_cell(0, 5, txt = text)
	pdf.cell(200, 15, txt = "", ln = 2, align = 'C')
	
	#add exNLP
	pdf.cell(200, 15, txt = "Most valuable sentences"+" "+"(Extractive Natural Language Processing)", ln = 2, align = 'C')
	text=myItem['mainText_exNLP'].encode('utf-8').decode('latin-1')
	filename= firstAuthor+'.pdf'	
	pdf.multi_cell(0, 5, txt = text)		
 
	# save the pdf with name .pdf	
	filePath=os.path.join(myItem['dirOfSummaries'][0], filename) 
	pdf.output(filePath)   
