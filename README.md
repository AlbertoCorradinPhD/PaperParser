# PaperParser
Corradin A., F. Ciccarese F., V. Raimondi V., L. Urso L., Ciminale V., Silic-Benussi M.. PaperParser: a bioinformatic tool that synthesizes scientific literature through advanced AI techniques, enhancing scholarly insights while mimicking human-like expression.  Proceedings of the 11th World Congress on New Technologies (NewTech'25). Paris, France, August, 2025. DOI: 10.11159/icbb25.161 

# Use
From Linux shell:
1) create new Python virtual environment
2) install Scrapy
3) test your Internet connection to PubMed database. For example by launching the following command:  'scrapy shell https://pubmed.ncbi.nlm.nih.gov/37076707/'
4) install needed Python modules, included pandas, bs4, sumy, fpdf, torch, transformers, rpy2
5) change direrctory to set the 'working dir' in correspondence of PaperParser, e.g. cd /home/.../paperParser/scraping_rev9
6) launch the Spider with the following command: 
scrapy crawl rev9 -a term=terms-of-search -s CLOSESPIDER_ITEMCOUNT=100, where terms-of-search represents the set of terms a user would insert in PubMed for a usual search in this database.

Then copy everything onto a cloud service like Google Drive for further data elaboration. Open file paperParserLLMs.ipynb with Google Colab and follow the commands reported in its cells.  
