library(qfa)
library(data.table)
inocdens=1E-5

# Read in colonyzer data, associate with metadata
raw=colonyzer.read(path="Output_Data",experiment="Auxiliary/ExptDescription.txt",ORF2gene="Auxiliary/ORF2Gene.txt",libraries="Auxiliary/LibraryDescription.txt",screenID="P15_cdc13-1")
# Define which measure of cell density to use for growth curves
raw$Growth=raw$Intensity
# Write data to file
write.table(raw,file="P15_QFA_Raw.txt",sep="\t",row.names=FALSE,quote=FALSE)

# Fit population models to data
# We can fit logistic model
fit=qfa.fit(raw,inocguess=inocdens,ORF2gene="Auxiliary/ORF2Gene.txt",minK=0.025,detectThresh=5e-4,fixG=TRUE,firstBarcode=FALSE,AUCLim=3.0,STP=5.0,glog=FALSE,modelFit=TRUE)
# Or generalised logistic model to give better fit to data (but parameter values harder to interpret and more variable)
gfit=qfa.fit(raw,inocguess=inocdens,ORF2gene="Auxiliary/ORF2Gene.txt",minK=0.025,detectThresh=5e-4,fixG=TRUE,firstBarcode=FALSE,AUCLim=3.0,STP=5.0,glog=TRUE,modelFit=TRUE)
# Use population model parameters to define a range of fitnesses
fit=makeFitness(fit)
gfit=makeFitness(gfit)
# Set default fitness
fit$fit=fit$MDRMDP
gfit$fit=gfit$MDRMDP
# Write fitness values to file
write.table(fit,file="P15_QFA_LogisticFitnesses.txt",sep="\t",row.names=FALSE,quote=FALSE)
write.table(gfit,file="P15_QFA_GeneralisedLogisticFitnesses.txt",sep="\t",row.names=FALSE,quote=FALSE)
# Plot growth curves.
qfa.plot("P15_QFA_LogisticGrowthCurves.pdf",fit,raw,maxg=0.25,maxt=3.0)
qfa.plot("P15_QFA_GeneralisedLogisticGrowthCurves.pdf",fit,raw,maxg=0.25,maxt=3.0)

