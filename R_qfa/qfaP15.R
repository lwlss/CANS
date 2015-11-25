# Working directory should be CANS
# setwd("F:\\CANS")

# Run these to install packages
#install.packages(c("knitr","DEoptim","sp","quantreg"))
#install.packages("qfa", repos="http://R-Forge.R-project.org")

library(qfa)
source("F:\\QFA\\pkg\\qfa\\R\\colonyRead.R")
source("F:\\QFA\\pkg\\qfa\\R\\qfa.R")

raw=colonyzer.read(
path=file.path("data","Output_Data"),
experiment=file.path("data","Auxiliary","ExptDescription.txt"),
ORF2gene=file.path("data","Auxiliary","ORF2GENE.txt"),
libraries=file.path("data","Auxiliary","LibraryDescription.txt")
)
raw$Growth=raw$Intensity

fit=control.fit<-qfa.fit(raw,inocguess=1E-4,ORF2gene=file.path("data","Auxiliary","ORF2GENE.txt"),AUCLim=4.0,STP=1.0,glog=FALSE,modelFit=TRUE)
fit=makeFitness(fit)
qfa.plot(file.path("R_qfa","R_qfa_GrowthCurves.pdf"),fit,raw,maxt=5)

write.table(fit,file=file.path("R_qfa","R_qfa_results.txt"),sep="\t",row.names=FALSE,quote=FALSE)



