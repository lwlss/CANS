library(data.table)

fitfile="MQFQFA0173_FIT.txt"
rawfile="MQFQFA0173_Raw.txt"

fit=fread(fitfile,sep="\t",stringsAsFactors=FALSE)
raw=fread(rawfile,sep="\t",stringsAsFactors=FALSE)

barcs=c("K000343_027_001","K000347_027_022")
fitkeeps=fit$Barcode%in%barcs
fit=fit[fitkeeps,]
rawkeeps=fit$Barcode%in%barcs
raw=raw[rawkeeps,]

write.table(fit,file="Stripes_FIT.txt",quote=FALSE,row.names=FALSE,sep="\t")
write.table(raw,file="Stripes_RAW.txt",quote=FALSE,row.names=FALSE,sep="\t")