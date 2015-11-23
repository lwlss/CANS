__author__ = 'victoriatorrance'


import openpyxl as op
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

wb2 = op.load_workbook('../gPROMS_output/gPROMS_output constant.xlsx')
print wb2.get_sheet_names()

def convertind(ind, NCol):
    '''Converts row-major vector index into row i and col j'''
    row = ind//NCol
    col = ind - row * NCol
    return((row + 1, col + 1))

def convertij(pos, NCol = 24):
    '''Converts row i, col j into row-major vector index'''
    i = pos[0]
    j = pos[1]
    return((i - 1) * NCol + (j - 1))


NCol = 12

sheet_ranges = wb2['Statistical Significance']
t = (sheet_ranges['B8':'B303'])

listInts = [sheet_ranges[str('B%i'%(item))].value for item in range(8, 152)]
listInts_only = []
listIJs = []
listInts_new =[]

for i in listInts:
    m = i.split('(')
    t = m[1].split(')')
    number = int(t[0])
    listInts_only.append(number)
    IJ = convertind(number-1, NCol)
    listIJs.append(IJ)
    IntNew = convertij(IJ, 24)
    listInts_new.append(IntNew+1)

f=pd.read_csv("../../data/ColonyzerOutput.txt",sep="\t")
intensity, ExptTime, Column, Row, geneName  = f["Intensity"], f["ExptTime"], f["Column"], f["Row"], f["Gene"]

# convert columns to indexes
ColRow = zip(Row, Column)
indexes = [1+(convertij(i)) for i in ColRow]

tot = zip(indexes, intensity, ExptTime, geneName, ColRow)
# store Intensity ad ExptTime readings in a dict with the index as key
mydict = {}

for a in indexes:
    mydict[str(a)] = []

for i in tot:
    mydict[str(i[0])] = mydict[str(i[0])] + ([i[2], i[1], i[3], i[4]])

geneList = []
for x in listInts_new:
    t = mydict['%i'%(x)]
    gene = t[2]
    colrow = t[3]
    geneList.append(gene+str(colrow))

index = 8
for gen in geneList:
    sheet_ranges['C%i'%(index)] = gen
    index += 1

wb = wb2

listInts = [sheet_ranges[str('B%i'%(item))].value for item in range(8, 152)]
listGeneNames = [sheet_ranges[str('C%i'%(item))].value for item in range(8, 152)]
listGeneNames2 = [name.split('(')[0] for name in listGeneNames]
listRvalues = [sheet_ranges[str('E%i'%(item))].value for item in range(8, 152)]

geneNamesUnique = set(listGeneNames2)

zippedInfo = zip(listInts, listGeneNames2, listRvalues)
mydataframe3 = pd.DataFrame(zippedInfo, columns=['pos', 'Gene', 'Fitness'] )
mydataframeSort =mydataframe3.sort('Fitness', ascending=0)



'''
dictnames = {}
for name in geneNamesUnique:
    dictnames[str(name)] = []
for i in zippedInfo:
    dictnames[str(i[1])] = dictnames[str(i[1])] + ([(i[2])])

for thegene in dictnames:
    m = sum(dictnames[thegene]) / float(len(dictnames[thegene]))
'''



ax = sns.boxplot(x="Gene", y="Fitness", data=mydataframeSort)
plt.xlabel('Gene', fontsize=7)
plt.show()


#for name in listGeneNames:

# Save the file
wb.save("sample.xlsx")
