# python 3.6
import glob
import os
import pandas as pd
path = ""

##_VERSION1_##
# create empty variable
newlist = []
# OS.walk() generate the file names in a directory tree by walking the tree either top-down or bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple (dirpath, dirnames, filenames).
# root : Prints out directories only from what you specified.
# dirs : Prints out sub-directories from root.
# files : Prints out all files from root and directories.
for root, dirs, files in os.walk(".", topdown=False):
    for filename in files:
        if filename.endswith('.xlsx') and filename.startswith('admon'):
            filedata = os.path.abspath(os.path.join(root, filename))
            df = pd.read_excel(filedata, sheet_name='admonAdops')
            newlist.append(df)

newlist = pd.concat(newlist, sort=False)
newlist.to_excel('ALL_admon1.xlsx')


##_VERSION 2_##
# merge/concat all dataframe to ALLDF
ALLDF = []
# define folder using specific character
# ilustration : we have some folder with same preprosition ([Toyota AM ...])
# get folder with spesific character
for folder in glob.glob('[Toyota AM*'):
    # define and match string/char in list directory from path dir
    if folder in os.listdir(path):
        # join names of folder with path dir
        # we have same of names folder from multiple directory, name folder is "admon"
        # so we append all directory with '/admon
        res = os.path.join(path, folder) + '/admon'
        # loop all listdir
        for file in os.listdir(res):
            # join every name of file with full directory
            # os.path.abspath are give full of file names
            pathFIle = [os.path.abspath(os.path.join(res, file))]
            for filedata in pathFIle:
                # read all file with directory name from pathFile
                data = pd.read_excel(filedata, sheet_name='admonAdops')
                # append all dataframe to ALLDF
                ALLDF.append(data)

# concat all dataframe of ALLDF
ALLDF = pd.concat(ALLDF, sort=False)
# save ALLDF to excel
ALLDF.to_excel('ALL_admon1.xlsx')
