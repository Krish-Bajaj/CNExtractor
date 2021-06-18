import pdfplumber as PDF
from data_extraction import getData

# with 'with' -> .close() doesn't need to be mentioned
try:
    with PDF.open('../files/amararaja.pdf') as pdf:
        data = getData(pdf)
        print(data["data"])
except:
    password = input("PDF is encrypted!\nEnter password: ")
    try:
        with PDF.open('../files/amararaja.pdf', password=password) as pdf:
            data = getData(pdf)
            print(data["data"])
    except:
       print("Password entered is incorrect!")
