import pdfplumber as PDF
from data_extraction import getData, getPDFs
from fetch_emails import getContractNotes
import pandas as pd

getContractNotes()

# with 'with' -> .close() doesn't need to be mentioned
data_list = []
try:
    file_list = getPDFs('../files')
    for file in file_list:
        with PDF.open('../files/{}'.format(file)) as pdf:
            data = getData(pdf)
            data_list.append(data["data"])

    df = pd.DataFrame(data_list)
    df.to_excel('trades.xlsx')
except:
    file_list = getPDFs('../files')
    for file in file_list:
        # password = input("PDF is encrypted!\nEnter password: ")
        try:
            with PDF.open('../files/{}'.format(file), password="KRI0106") as pdf:
                data = getData(pdf)
                data_list.append(data["data"])
        except:
            print("Password entered is incorrect!")
    df = pd.DataFrame(data_list)
    df.to_excel('trades.xlsx')