import PyPDF2 as PDF

pdf = open('../files/sample.pdf', 'rb')
pdfReader = PDF.PdfFileReader(pdf)

firstPage = pdfReader.getPage()
print(firstPage.extractText())