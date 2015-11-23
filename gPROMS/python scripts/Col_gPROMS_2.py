__author__ = 'victoriatorrance'

import pandas as pd

predict = 1.5 # initial predicted r value
lower = 0.5 # lower bound prediction
upper = 6.5 # upper bound prediction

### can also go into the script and change the varience initial lower and upper

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

nrow, ncol = 3, 7
totalSpots = nrow * ncol
listOfInts = [x for x in range(0, totalSpots)]

list_indexes = [convertind(x, ncol) for x in listOfInts]

f=pd.read_csv("/Users/victoriatorrance/Desktop/ColonyzerOutput_2.txt",sep="\t")
intensity, ExptTime, Column, Row  = f["Intensity"], f["ExptTime"], f["Column"], f["Row"]

# convert columns to indexes
ColRow = zip(Row, Column)
indexes = [1+(convertij(i)) for i in ColRow]

tot = zip(indexes, intensity, ExptTime)

performed_exp = open("performed_exp.txt", "w")


# store Intensity ad ExptTime readings in a dict with the index as key
mydict = {}

for a in indexes:
    mydict[str(a)] = []

for i in tot:
    mydict[str(i[0])] = mydict[str(i[0])] + ([(i[2], i[1])])


nrow_reduced = 7
ncol_reduced = 7
itemid = 1



for a in range(1, 385):
    coords = convertind(a-1, 24)
    # Only extracted data within the reduced-size plate
    if(coords[0] > nrow_reduced or coords[1] > ncol_reduced):
        pass
    else:
        performed_exp.write( 'MEASURE' + '\n' + "Flowsheet.my_model.C(%i)" % itemid +'\n')
        for a in mydict[str(a)]:
            performed_exp.write( str(a[0]) + '\t'+ str(a[1]) +'\n')
        performed_exp.write('\n\n')
        itemid += 1


performed_exp.close()


totred = ncol_reduced * nrow_reduced
parameter_est = open("parameter_est.txt", "w")

for item in range (1, totred+1):
    parameter_est.write("ESTIMATE"+'\n'+'Flowsheet.my_model.pos(%i)'%(item)+'\n'+ str(predict)+' : '+str(lower)+' : '+str(upper)+'\n\n')

parameter_est.write('\n\n\n'+"MEASUREMENT_GROUP"+'\n'+'CONSTANT_VARIANCE (0.01 : 1.0E-8 : 1.0)'+'\n')

for x in range (1, totred+1):
    parameter_est.write("SENSOR"+'\n'+'Flowsheet.my_model.C(%i)'%(x)+'\n'+'EXPERIMENTS'+'\n'+'my_model'+'\n\n')
parameter_est.close()

print "FINISHED"



