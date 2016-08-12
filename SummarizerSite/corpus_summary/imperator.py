"""
This python file will actuate text analysis of corpuses of text from libros_epitome.py
"""

from libros_epitome import summarize_from_raw_text, summarize_from_rss_feeds
import PyPDF2
import glob

pdf_list = glob.glob('/home/issacs/Desktop/Corpus_Analyzer/documents/*.pdf')
print(pdf_list)
for i in pdf_list:
    pdf_file_object = open(i, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)
    text = ''
    for j in range(pdf_reader.numPages):
        text += pdf_reader.getPage(j).extractText()
    summarize_from_raw_text(
        text,
        i.split('/')[len(i.split('/')) - 1], 
        pdf_reader.numPages
    )

#summarize_from_raw_text(raw_text, 'FREE PRIVATE CITIES: THE FUTURE OF GOVERNANCE IS PRIVATE')

