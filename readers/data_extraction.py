import pdfplumber as PDF
import re
import os
import datetime

def getData(pdf):
    # to get a particular page -> pdf.pages[0]
    types_of_PDF = ['CONTRACT NOTE', 'Contract Note', 'TAX INVOICE']
    pages = pdf.pages
    text_version = ""
    for page in pages:
        pageData = page.extract_text()
        text_version += pageData

    # flow for checking if it's the correct type of document
    is_correct_type = False
    for type in types_of_PDF:
        if type in text_version:
            is_correct_type = True
            break

    if is_correct_type:
        data = {}
        text_lines = []
        for sublist in text_version.split('\n'):
            text_lines.append(sublist)
        # f = open("persistent.txt", "w")
        # f.write(text_version)

        # # code to get name
        # pattern = '^Name(.*)SEBI'  # '()' means we want stuff only between that
        # for line in text_lines:
        #     if line.startswith("Name"):
        #         name = re.findall(pattern, line)[0].strip()
        #         data["Name"] = name
        #         break

        # code to get settlement date
        settlement_pattern = 'SETTLEMENT DATE(.*)'
        month_pattern = '[a-zA-Z]+'
        year_pattern = '\-(\d+)'
        for line in text_lines:
            if "SETTLEMENT DATE" in line:
                settlement_date = re.findall(settlement_pattern, line)[0].strip().upper()

                # get all the years in the same format (doing this before month to month num
                # change for easier pattern identification)
                year = re.findall(year_pattern, settlement_date)[0]
                if len(year) == 2:
                    new_year = "20" + year
                else:
                    new_year = year
                settlement_date = settlement_date.replace(year, str(new_year))

                # replacing month with month number
                month = re.findall(month_pattern, settlement_date)[0]
                month_num = datetime.datetime.strptime(month, "%b").month
                settlement_date = settlement_date.replace(month, str(month_num))

                # https://www.geeksforgeeks.org/python-sort-list-of-dates-given-as-strings/

                data["Settlement Date"] = settlement_date
                break

        # get name of the stock
        stock_pattern = '^Equity(.*)-C'
        # get quantity bought or sold
        quantity_pattern = '\s(\d+)'
        # get total amount
        amount_pattern = '\d+\.\d+'

        for line in text_lines:
            if line.startswith("Equity"):
                stock = re.findall(stock_pattern, line)[0].strip()
                data["Stock"] = stock

                quantity = re.findall(quantity_pattern, line)
                data["Quantity (Bought)"] = quantity[0]
                data["Quantity (Sold)"] = quantity[1]

                words = line.split()
                amount = re.findall(amount_pattern, words[len(words) - 1])[0]
                data["Amount"] = amount
        
        # price per share
        pps = float(data["Amount"])/(int(data["Quantity (Bought)"]) + int(data["Quantity (Sold)"]))
        data["Price per share"] = "{:.2f}".format(pps) # keeping only 2 decimal places
                
    return {"data": data, "is_correct_type": is_correct_type}

# returns all the files in the "files" directory
def getPDFs(directory):
    file_list = []
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            file_list.append(file)
    return file_list