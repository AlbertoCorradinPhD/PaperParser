
import os
import re

def storeSources(myItem,firstAuthor, main=False):

	filename= firstAuthor+'.txt'
	if main:
		filePath=os.path.join(myItem['dirOfMainTexts'][0], filename) 
	else:	
		filePath=os.path.join(myItem['dirOfAbstracts'][0], filename) 

	
	with open(filePath, 'wt') as outfile:
		
		if main:
			text="\n\n"+myItem['mainText'].encode('utf-8').decode('latin-1')
		else:			
			text= "\n\n"+myItem['title'][0].encode('utf-8').decode('latin-1')
			outfile.write(text)
			text="\n\n"+myItem['authors'][0].encode('utf-8').decode('latin-1')
			outfile.write(text)
			text="\n\n"+'Journal: '+myItem['journal'][0].encode('utf-8').decode('latin-1')
			outfile.write(text)
			text="\n\n"+'Date of publication: '+myItem['year'][0].encode('utf-8').decode('latin-1')
			outfile.write(text)				
			text="\n\n"+myItem['abstract'][0].encode('utf-8').decode('latin-1')
		
		outfile.write(text)
		outfile.close()
