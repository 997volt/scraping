import os
from PyPDF2 import PdfFileReader, PdfFileWriter

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

print("Welcome to pdf pages adding tool - choose a pdf file to modify.")

path = '/home/user/Downloads/etykieta.pdf'
print('Opening default file' + path)

#Tk().withdraw()
#path = askopenfilename()
#print("Your file is - " + path)
#print("Adding 1 page before document")
#beforeAter = input("Do you want to write blank page after or before decoument (write 'a' or 'b'): ")
#numberOfPages = input("How many pages do you want to add: ")

pdf = PdfFileReader(path)
pdf_writer = PdfFileWriter()

pdf_writer.addBlankPage(pdf.getPage(0).mediaBox[2], pdf.getPage(0).mediaBox[3])
for page in range(pdf.getNumPages()):
    pdf_writer.addPage(pdf.getPage(page))

with open(path[:-4] + "_mod.pdf", 'wb') as out:
    pdf_writer.write(out)

print("Success! New file created.")
