import pandas as pd
import numpy as np
import os

imOutDir="../data/Output_Data"
exptDesc="../data/ExptDescription.txt"
libDesc="../data/LibraryDescription.txt"
geneToORF="../data/ORF2GENE.txt"
fout="../data/RawData.txt"
fmt="%Y-%m-%d_%H-%M-%S"

def parseColonyzer(fname):
    '''Read in Colonyzer .out file and parse some info from filename.'''
    froot=os.path.basename(fname).split(".")[0]
    barc=froot[0:-20]
    datetime=froot[-19:]
    data=pd.read_csv(fname,sep="\t",header=0)
    data["Barcode"]=barc
    data["DateTime"]=datetime
    data["FileName"]=froot
    return(data)

def getORF(libs,Library,Plate,Row,Column):
    '''Get ORF at a given row, column and plate in a particular QFA library, found in dataframe libs describing all available libraries.'''
    filt=libs.ORF[(libs.Library==Library)&(libs.Plate==Plate)&(libs.Row==Row)&(libs.Column==Column)]
    return(filt.get_values()[0])

# Read in and combine all .out files
imList=os.listdir(imOutDir)
outs=[parseColonyzer(os.path.join(imOutDir,out)) for out in imList if ".out" in out]
ims=pd.concat(outs)

# Read in experimental metadata
expt=pd.read_csv(exptDesc,sep="\t",header=0)

# Read in library description file
libs=pd.read_csv(libDesc,sep="\t",header=0)
libs.columns=[x.rstrip() for x in libs.columns]

# Read in file describing link between standard gene name and systematic gene name (ORF) as python dictionary orf2g
g2orf_df=pd.read_csv(geneToORF,sep="\t",header=None)
orf2g=dict(zip(g2orf_df[0],g2orf_df[1]))

# Add metadata from expt to ims
ims["Start.Time"]=expt["Start.Time"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Treatment"]=expt["Treatment"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Medium"]=expt["Medium"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Screen"]=expt["Screen"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Library"]=expt["Library"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Plate"]=expt["Plate"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["RepQuad"]=expt["RepQuad"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]

# Calculate time since inoculation date time (from expt metadata) that image was taken
ims["ExptTime"]=(pd.to_datetime(ims["DateTime"],format=fmt)-pd.to_datetime(ims["Start.Time"],format=fmt))/np.timedelta64(1,"D")

# Get ORFs at each position from relevant library description
ims["ORF"]=[getORF(libs,l,p,r,c) for l,p,r,c in zip(ims.Library,ims.Plate,ims.Row,ims.Column)]
# Get standard gene names for each ORF
ims["Gene"]=[orf2g[orf] for orf in ims.ORF]

# Write data, metadata and newly calulated times to file
ims.to_csv(fout,sep="\t")






