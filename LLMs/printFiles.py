import os
from fpdf import FPDF

def printPDF(name, text, resultsDir):	
	"""
	Print on RESULTS directory only
	"""
	
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size = 10)

	text=text.encode('utf-8').decode('latin-1')
	pdf.multi_cell(0, 5, txt = text)
	# save the pdf with name .pdf

	output_filename=name+".pdf"
	filePath=os.path.join(resultsDir, output_filename)
	pdf.output(filePath)
	print("Printed output file:")
	print(filePath)
	
def printTXT(output_filename, outputDirPath, title, text):
	"""
	Print where specified
	"""
	
	output_path=os.path.join(outputDirPath,output_filename)
	with open(output_path, 'wt') as outfile:
		outfile.write(str(title))
		outfile.write("\n\n")
		outfile.write(str(text))
		outfile.close()

