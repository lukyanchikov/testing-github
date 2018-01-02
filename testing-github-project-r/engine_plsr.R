# TODO: Add comment
# 
# Author: Sergey
###############################################################################

e=read.csv("file:///C:/Users/Sergey/Documents/Programing/R/OSIsoft/EngineView_20160929074014_adjusted.csv",header=T, sep="\t")
colnames(e)[1]="Internal"
e$engine=as.numeric(gsub("Engine_","",e$engine))
e=subset(e,select=-c(Internal,PIIntTSTicks,PIIntShapeID))
e=subset(e,select=-c(setting3,s1,s5,s10,s16,s18,s19))
e.fail=tapply(e$cycle,e$engine,max)
e$rul=e.fail[e$engine]-e$cycle
e.odd=subset(e,e$engine%%2==1)
e.even=subset(e,e$engine%%2==0)
library(pls)
e.odd.plsr=plsr(rul~., ncomp = 5, data = e.odd, validation = "LOO")
predplot(e.odd.plsr, ncomp = 2, newdata = e.even, asp = 1, line = TRUE)