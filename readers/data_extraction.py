import pdfplumber as PDF
import re


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

        # code to get name
        pattern = '^Name(.*)SEBI'  # '()' means we want stuff only between that
        for line in text_lines:
            if line.startswith("Name"):
                name = re.findall(pattern, line)[0].strip()
                data["Name"] = name
                break

        # regex to get name of the stock
        stock_pattern = '^Equity(.*)-C'
        # regex to get quantity bought or sold
        quantity_pattern = '(\d+)\s'
        # regex to get total amount bought or sold
        amount_pattern = '\((\d+\.\d+)'
        for line in text_lines:
            if line.startswith("Equity"):
                stock = re.findall(stock_pattern, line)[0].strip()
                data["Stock"] = stock

                quantity = re.findall(quantity_pattern, line)
                data["Quantity (Bought)"] = quantity[0]
                data["Quantity (Sold)"] = quantity[1]

                amount = re.findall(amount_pattern, line)[0].strip()
                data["Amount"] = amount
                

    return {"data": data, "is_correct_type": is_correct_type}
