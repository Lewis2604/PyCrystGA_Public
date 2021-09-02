# User needs to download ElementTree and Pandas
# User needs blank xml file and excel spreadsheet



# import element tree xml parser
# import pandas for dataframes

import xml.etree.ElementTree as ET
import pandas as pd

# specify xml document to parse (blank on group drive)

tree = ET.parse(r'C:\Users\Lewis\Downloads\XML_Blank.xml')
root = tree.getroot()

print("t")
print(tree)
print('r')
print(root)

# open user input excel file (blank on group drive)

excel = open(r'C:\Users\Lewis\Downloads\XML_Excel.xlsx', 'r')

# read excel into a data frame and print

df1 = pd.read_excel(r'C:\Users\Lewis\Downloads\XML_Excel.xlsx', sheet_name = 'Sheet1')
print("Dataframe")
print(df1)


# store columns in data frame as variables

skip = df1['Skip']
state = df1['State']
loc = df1['LocationId']
sid = df1['SampleId']
prog = df1['XDCBatchProgram']

# print(loc[2])


# iterate through xml and modify xml according to dataframe

i = 0
for elem in root.iter('LocationId'):
    if i < len(loc):
        elem.text = loc[i]
        i += 1


s = 0
for elem in root.iter('SampleId'):
    if s < len(sid):
        elem.text = sid[s]
        s += 1


p = 0
for elem in root.iter('XDCBatchProgram'):
    if p < len(sid):
        elem.text = prog[p]
        p += 1

x = 0
for elem in root.iter('Skip'):
    if x < len(skip):
        elem.text = str(skip[x])
        x += 1

y = 0
for elem in root.iter('State'):
    if y < len(state):
        elem.text = state[y]
        y += 1


# save result as a new xml file

tree.write(r'C:\Users\Lewis\Downloads\newxml.xml')

