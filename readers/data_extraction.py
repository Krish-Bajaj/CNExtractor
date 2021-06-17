import pdfplumber as PDF


def getData(pdf):
    # to get a particular page -> pdf.pages[0]
    types_of_PDF = ['CONTRACT NOTE', 'TAX INVOICE']
    # for page in pdf.pages:
    #     print(page.extract_text()) # prints text on all pages
    page = pdf.pages[0]
    pageData = page.extract_text()
    is_correct_type = False
    for type in types_of_PDF:
        if type in pageData:
            is_correct_type = True
            break

    return {"pageData": pageData, "is_correct_type": is_correct_type}
