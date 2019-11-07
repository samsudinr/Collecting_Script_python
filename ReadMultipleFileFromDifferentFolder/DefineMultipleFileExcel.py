import os
import pandas as pd

def create_new_sheet(filedata, sheetname):
    newlist = []
    for root, dirs, files in os.walk(".", topdown=False):
        for filename in files:
            if filename.endswith('.xlsx') and filename.startswith('admon'):
                file = os.path.abspath(os.path.join(root, filename))
                df = pd.read_excel(file, sheet_name=sheetname)
                newlist.append(df)
    newlist = pd.concat(newlist, sort=False)
    newlist.to_excel(filedata, sheet_name=sheetname, index=False)


if __name__ == '__main__':
    filedata = pd.ExcelWriter('newfile1.xlsx')
    create_new_sheet(filedata, 'admonAdops')
    create_new_sheet(filedata, 'channelToReview')
    create_new_sheet(filedata, 'CreToReview')
    filedata.save()
    filedata.close()
