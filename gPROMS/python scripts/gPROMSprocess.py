__author__ = 'victoriatorrance'

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st


# Some Information about the file
NCol = 24
noDataPoints = 384

# Edit the following so that the file can be parsed correctly.
#  NEED TO OPEN THE FILE YOU WANT TO PROCESS AND CHECK WHAT THESE ARE

lowerBound = '0  '  #MUST CONTAIN A TOTAL OF 3 SPACES
upperBound = '6.5'  #MUST CONTAIN A TOTAL OF 3 SPACES


#Functions that we need
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

# we need to open the Colonyzer Output file so that we can remember what the names of all these genes are.
#f=pd.read_csv("/Users/victoriatorrance/Desktop/ColonyzerOutput_2.txt",sep="\t")
f=pd.read_csv("../../data/ColonyzerOutput.txt",sep="\t")
intensity, ExptTime, Column, Row, geneName  = f["Intensity"], f["ExptTime"], f["Column"], f["Row"], f["Gene"]

# convert columns to indexes
ColRow = zip(Row, Column)
indexes = [1+(convertij(i)) for i in ColRow]

# zip together our indexes with other info including ColRow and genename. Now each index has a gene name
tot = zip(indexes, intensity, ExptTime, geneName, ColRow)

# make a dictionary which contains as the key the index number and as the item, the gene name
mydict = {}

for a in indexes:
    mydict[str(a)] = []

for i in tot:
    mydict[str(i[0])] = mydict[str(i[0])] + ([i[3]])

# open up gPROMS output text file!
#f = open("/Users/victoriatorrance/Desktop/gPROMS example Parameter Estimation copy.txt")
#f = open("my_model.txt")
f = open("../../data/gPROMS example Parameter Estimation.txt")
f=list(f)


# Some things we need to do to parse this difficult to read gPROMS text file.

myinfo = [line for line in f[18:noDataPoints+20] ]

itemToRemove = myinfo[1]

myinfo.remove(itemToRemove)

newlist_Parameters = []
newlist_Value = []

for x in myinfo[1:(len(myinfo))]:
    xsplit = x.split('%s        %s'%(lowerBound, upperBound))[0]
    xsplit2 = xsplit.split(')')
    name = xsplit2[0]+')'
    r_value = xsplit2[1]
    newlist_Parameters.append(name)
    newlist_Value.append(r_value)

# We now have two nice lists which contain a list of parameter names, and a list of R values
# we need to however match up there parameter names (which contain index numbers) which the gene names
# we also need to tidy up newlist_value (containing the r value estimates)

listInts_only = []
listIJs = []
listInts_new =[]
listGeneNames = []


for i in newlist_Parameters:
    m = i.split('(')
    t = m[1].split(')')
    #extract the index and put in a list
    number = int(t[0])
    listInts_only.append(number)
    # use Conors function to obtain a list of co-ords for each of our indexes
    # we only really need to do this if we are dealing with different numbers of stains
    IJ = convertind(number-1, NCol)
    listIJs.append(IJ)
    # by creating a list of new indexes this ensures that we have the correct index number even if dealing with different sized plates
    IntNew = convertij(IJ, 24)
    listInts_new.append(IntNew+1)
    # Look up the gene name for each number and append it to a separate list
    GeneName = mydict[str(IntNew+1)][0]
    listGeneNames.append(GeneName)

# tidy up the list of r values. remove all spaces and turn numbers into floats
newlist_Value_Floats = []

for x in newlist_Value:
    xNumber = x.replace(' ','')
    newlist_Value_Floats.append(float(xNumber))

# zip togther all of the important information, geneNames, r estimates
#  and just incase we want to check everything is working we shall keep the gPROMS identifier for each gene and r estimate

zippedInfo = zip(listGeneNames, newlist_Parameters, newlist_Value_Floats)
mydataframe = pd.DataFrame(zippedInfo, columns=['Gene','Parameter', 'Value'] )
mydataframeSort = mydataframe.sort_values('Value', ascending=0)

# mydataframe is fine if we want to view boxplots and mydataframeSort boxplots will sort by the r value but
   # it is not perfect. we really want to sort by medians. this is a bit more tricky.

# We need to add another collumn to the dataframe which contains a Median value of all the r_estimates for that given gene...
# this way we can sort them easily

#create a new dict which contains the gene names as the keys and the r values as the items. some keys(genes)
# will have multiple r values per key.. eg HIS

geneNamesUnique = set(listGeneNames)

dictnames = {}
for name in geneNamesUnique:
    dictnames[str(name)] = []

for i in zippedInfo:
    dictnames[str(i[0])] = dictnames[str(i[0])] + ([(i[2])])

# we loop through our dict and calculate the median for each set of r estimates corresponding to each gene
# we end up with a zipped list containing GeneName and med value of the r estimates for that given gene
gen,medians = [],[]

for thegene in dictnames:
    gen.append(thegene)
    med = st.median(dictnames[thegene])
    medians.append(med)

geneAndMed = zip(gen, medians)

# But now we know for each gene what the median of its' r estimates are we need to incorporate this information into
    # our dataframe

# create a list of Median values which is in the same order as our listGeneNames
listMEDS = []

for x in zippedInfo:
    for y in geneAndMed:
        if x[0] == y[0]:
            listMEDS.append(y[1])

zippedinfoMeds = zip(listGeneNames, newlist_Parameters, newlist_Value_Floats, listMEDS)

#bp = sns.barplot(x="Median", y="Gene", data=AveragedDataFrameSort)


mydf = pd.DataFrame(zippedinfoMeds, columns=['Gene', 'parameter','Fitness', 'Median'])
myDFsort = mydf.sort_values('Median',ascending=0)
print myDFsort
   # dictaverages[str(thegene[0])] = dictaverages[str(thegene[0])] + ([(mstr)])

#print mydataframe

ax = sns.boxplot(x="Fitness", y="Gene", data=myDFsort, orient= "h")
#ax = sns.stripplot(x="Fitness", y="Gene", data=myDFsort,size=3, jitter=True, edgecolor="gray")
#ax = sns.barplot(x="Fitness", y="Gene", data=myDFsort)
ax = sns.stripplot(x="Fitness", y="Gene", data=myDFsort,size=3, jitter=True, edgecolor="gray")

plt.xlim(-0.05, 4)
plt.savefig("Boxplot of Fitness estimates.pdf")
plt.show()