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
    froot=os.path.basename(fname).split(".")[0]
    barc=froot[0:-20]
    datetime=froot[-19:]
    data=pd.read_csv(fname,sep="\t",header=0)
    data["Barcode"]=barc
    data["DateTime"]=datetime
    data["FileName"]=froot
    return(data)   

imList=os.listdir(imOutDir)
outs=[parseColonyzer(os.path.join(imOutDir,out)) for out in imList if ".out" in out]
ims=pd.concat(outs)

expt=pd.read_csv(exptDesc,sep="\t",header=0)

lib=pd.read_csv(libDesc,sep="\t",header=0)
lib.columns=[x.rstrip() for x in lib.columns]

g2orf_df=pd.read_csv(geneToORF,sep="\t",header=None)
orf2g=dict(zip(g2orf_df[0],g2orf_df[1]))

ims["Start.Time"]=expt["Start.Time"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Treatment"]=expt["Treatment"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Medium"]=expt["Medium"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Screen"]=expt["Screen"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Library"]=expt["Library"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["Plate"]=expt["Plate"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]
ims["RepQuad"]=expt["RepQuad"][expt.Barcode==ims.Barcode.unique()[0]].get_values()[0]

ims["ExptTime"]=(pd.to_datetime(ims["DateTime"],format=fmt)-pd.to_datetime(ims["Start.Time"],format=fmt))/np.timedelta64(1,"D")

def getORF(lib,Library,Plate,Row,Column):
    filt=lib.ORF[(lib.Library==Library)&(lib.Plate==Plate)&(lib.Row==Row)&(lib.Column==Column)]
    return(filt.get_values()[0])

ims["ORF"]=[getORF(lib,l,p,r,c) for l,p,r,c in zip(ims.Library,ims.Plate,ims.Row,ims.Column)]
ims["Gene"]=[orf2g[orf] for orf in ims.ORF]

ims.to_csv(fout,sep="\t")






