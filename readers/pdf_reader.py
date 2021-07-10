import pdfplumber as PDF
from .data_extraction import getData, getPDFs, deletePDFs
from .fetch_emails import getContractNotes
import pandas as pd
import os

def generateData():
    getContractNotes()

    # opening a file with 'with' -> .close() doesn't need to be mentioned
    data_list = []
    date_list = []
    try:
        file_list = getPDFs('files')
        for file in file_list:
            with PDF.open('files/{}'.format(file)) as pdf:
                data = getData(pdf, date_list)
                data_list.append(data["data"])

    except:
        file_list = getPDFs('files')
        for file in file_list:
            password = input("PDF is encrypted!\nEnter password: ")
            try:
                with PDF.open('files/{}'.format(file), password=password) as pdf:
                    data = getData(pdf, date_list)
                    data_list.append(data["data"])
            except:
                print("Password entered is incorrect!")

    df = pd.DataFrame(data_list)
    # df.to_excel('trades.xlsx')
    # deletePDFs('files')
    # os.remove('gmail_token.json')
    return data_list
