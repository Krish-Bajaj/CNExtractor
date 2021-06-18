import pdfplumber as PDF
from data_extraction import getData, getPDF

# with 'with' -> .close() doesn't need to be mentioned
try:
    file_list = getPDF('../files')
    for file in file_list:
        with PDF.open('../files/{}'.format(file)) as pdf:
            data = getData(pdf)
            print(data["data"])
except:
    file_list = getPDF('../files')
    for file in file_list:
        password = input("PDF is encrypted!\nEnter password: ")
        try:
            with PDF.open('../files/{}'.format(file), password=password) as pdf:
                data = getData(pdf)
                print(data["data"])
        except:
            print("Password entered is incorrect!")
