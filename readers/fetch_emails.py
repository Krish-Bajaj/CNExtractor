from simplegmail import Gmail
from simplegmail.query import construct_query
import os
import shutil


def getContractNotes():
    gmail = Gmail()

    # label_name = input("\nEnter your label under which files are stored: ")
    query_params = {
        "read": True,
        # "labels":[[label_name]],
        "after": "2020/02/27",
        "subject": "Contract Note for Acc No",
    }

    messages = gmail.get_messages(query=construct_query(query_params))
    for message in messages:
        if message.attachments:
            for attm in message.attachments:
                attm.save()

    # moves pdf files from current directory to emails folder
    for file in os.listdir():
        if file.endswith('.pdf'):
            shutil.move(file, "../files")