import pdfplumber as PDF
from data_extraction import getData

# with 'with' -> .close() doesn't need to be mentioned
try:
    with PDF.open('../files/combined.pdf') as pdf:
        data = getData(pdf)
except:
    password = input("PDF is encrypted!\nEnter password: ")
    try:
        with PDF.open('../files/combined.pdf', password=password) as pdf:
            data = getData(pdf)
    except:
       print("Password entered is incorrect!")
