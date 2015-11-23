import pandas as pd
import numpy as np
import os


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

def parseAndCombine(imOutDir=".",exptDesc="ExptDescription.txt",libDesc="LibraryDescription.txt",geneToORF="ORF2GENE.txt",fout="ColonyzerOutput.txt",fmt="%Y-%m-%d_%H-%M-%S"):
    '''Read in a list of colonyzer output files, together with optional metadata files describing inoculation times, strains, treatments applied etc. to produce one summary output file.'''
    # Read in and combine all .out files
    imList=os.listdir(imOutDir)
    outs=[parseColonyzer(os.path.join(imOutDir,out)) for out in imList if ".out" in out]
    ims=pd.concat(outs)

    
    try:
        # Read in experimental metadata
        expt=pd.read_csv(exptDesc,sep="\t",header=0)
    except:
        print(exptDesc+" not found, carrying on...")
        expt=None
        
    try:
        # Read in library description file
        libs=pd.read_csv(libDesc,sep="\t",header=0)
        libs.columns=[x.rstrip() for x in libs.columns]
    except:
        print(libDesc+" not found, carrying on...")
        libs=None

    try:
        # Read in file describing link between standard gene name and systematic gene name (ORF) as python dictionary orf2g
        g2orf_df=pd.read_csv(geneToORF,sep="\t",header=None)
        orf2g=dict(zip(g2orf_df[0],g2orf_df[1]))
    except:
        print(geneToORF+" not found, carrying on...")
        orf2g=None

    if expt is not None:
        # Add metadata from expt to ims
        ims["Start.Time"]=[expt["Start.Time"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["Treatment"]=[expt["Treatment"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["Medium"]=[expt["Medium"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["Screen"]=[expt["Screen"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["Library"]=[expt["Library"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["Plate"]=[expt["Plate"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]
        ims["RepQuad"]=[expt["RepQuad"][expt.Barcode==barc].get_values()[0] for barc in ims["Barcode"]]

        # Calculate time since inoculation date time (from expt metadata) that image was taken
        ims["ExptTime"]=(pd.to_datetime(ims["DateTime"],format=fmt)-pd.to_datetime(ims["Start.Time"],format=fmt))/np.timedelta64(1,"D")

        # Get ORFs at each position from relevant library description
        ims["ORF"]=[getORF(libs,l,p,r,c) for l,p,r,c in zip(ims.Library,ims.Plate,ims.Row,ims.Column)]

    if orf2g is not None and expt is not None:
        # Get standard gene names for each ORF
        ims["Gene"]=[orf2g[orf] for orf in ims.ORF]

    # Write data, metadata and newly calulated times to file
    ims.to_csv(fout,sep="\t")
    ims.to_csv(anotherfile,sep="\t")
    print ims
    return(ims)

if __name__ == "__main__":

    imOutDir=  "/Users/victoriatorrance/Documents/CANS/data/Output_Data" #"../data/Output_Data"
    exptDesc="/Users/victoriatorrance/Documents/CANS/data/Auxiliary/ExptDescription.txt"
    libDesc=  "/Users/victoriatorrance/Documents/CANS/data/Auxiliary/LibraryDescription.txt" #"../data/Auxiliary/LibraryDescription.txt"
    geneToORF= "/Users/victoriatorrance/Documents/CANS/data/Auxiliary/ORF2GENE.txt"
    fout= "/Users/victoriatorrance/Documents/CANS/data/RawData.txt"
    anotherfile= "/Users/victoriatorrance/Documents/CANS/data/anotherfile.txt"
    fmt="%Y-%m-%d_%H-%M-%S"
    #imOutDir="../data/Output_Data"
    #exptDesc="../data/Auxiliary/ExptDescription.txt"
    #libDesc="../data/Auxiliary/LibraryDescription.txt"
    #geneToORF="../data/Auxiliary/ORF2GENE.txt"
    #fout="../data/RawData.txt"
    #fmt="%Y-%m-%d_%H-%M-%S"

    res=parseAndCombine(imOutDir,exptDesc,libDesc,geneToORF,fout,fmt)


    print 'wow no errors'