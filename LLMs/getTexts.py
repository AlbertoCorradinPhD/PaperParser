import glob
import os
import datetime
from printFiles import printTXT

def read_content(file):
    with open(file, 'rt') as fd:
        content = fd.read()
        fd.close()
    return content

def get_mod_time(path):
  m_time = os.path.getmtime(path)
  dt = datetime.datetime.fromtimestamp(m_time)
  return dt

def merge_per_folder(folder_path, reverse=False):
    """Merges content of text files in one folder, and
    writes combined lines into new output file

    Parameters
    ----------
    folder_path : str
        String representation of the folder path containing the text files.
    output_filename : str
        Name of the output file the merged lines will be written to.
    """
    # make sure there's a slash to the folder path
    #folder_path += "" if folder_path[-1] == "/" else "/"
    # get all text files
    txt_files = glob.glob(folder_path + "/*.txt")
    #print(txt_files)
    
    # get content; map to each text file (sorted)
    output_strings = map(read_content, sorted(txt_files, key=lambda x: get_mod_time(x), reverse=reverse))
    output_content = "\n\n".join(output_strings)
    return output_content


def test_getTexts(path1, path2):

	print("Content:")
	print(read_content(path1))
	print("This file was modified last:")
	print(get_mod_time(path1))

	#test sorting method
	print("Second file was modified last:")
	print(get_mod_time(path2))

	txt_files=[path1, path2]
	print("Reverse sorting:")
	print(sorted(txt_files, key=lambda x: get_mod_time(x), reverse=True))
	print("Default sorting:")
	print(sorted(txt_files, key=lambda x: get_mod_time(x), reverse=False))

def mergeSummaries(outputDir, inputDir, suffixes):
	
	print("Output directory:")
	print(outputDir)
	folder_path=inputDir	
	AI_inputs=[]
	
	# direct order
	AI_input= merge_per_folder(folder_path, reverse=False)
	output_filename="AI_input"+suffixes[0]+".txt"
	printTXT(output_filename, outputDir, title='', text=AI_input)
	AI_inputs.append(AI_input)
	
	# reverse order
	AI_input= merge_per_folder(folder_path, reverse=True)
	output_filename="AI_input"+suffixes[1]+".txt"
	printTXT(output_filename, outputDir, title='', text=AI_input)
	AI_inputs.append(AI_input)
	
	return AI_inputs
