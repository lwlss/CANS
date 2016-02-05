from logistic_model import *
import seaborn as sns
import argparse
from matplotlib.backends.backend_pdf import PdfPages

def makeLong(df):
    longversion=pd.melt(df)
    metadata=longversion.variable.str.split("_",expand=True)
    longversion=pd.concat([longversion,metadata],axis=1)
    if len(longversion.columns)==5:
        longversion.columns=["fname",longversion[0][0],"var","gene","column"]
    else:
        longversion.columns=["fname",longversion[0][0],"var","column"]
    return(longversion)

def makeBoxplot(longdf):
    sns.set_context("poster",font_scale=1.5)
    var=longdf["var"][0]
    if "gene" in longdf.columns:
        ax = sns.boxplot(x="column",y=var,hue="gene",data=longdf,palette="Set3")
        if var=="K":
            ax.set_ylim(0,0.2)
        else:
            ax.set_ylim(0,6.5)
    else:
        ax = sns.boxplot(x="column",y=var,data=longdf)
        ax.set(yscale="log")
        ax.set_ylim(1e-4,)
        
    #plt.xticks(rotation=90)
    #plt.show()    

parser = argparse.ArgumentParser(description='Dilution Experiment')
parser.add_argument("-c","--column", type=int ,help='Plate column number')
parser.add_argument("-r","--report", help="Summarise completed inference",action="store_true")
args = parser.parse_args()

root="Dilutions"
fname="../../data/dilution/RawData.txt"

if args.column:
    colnum=int(args.column)
    print("Column {}".format(colnum))
    
    raw=pd.read_csv(fname,sep="\t")
    raw=raw[raw.Column==colnum]
    
    make_sure_path_exists(root)
    dirname=os.path.join(root,"C{0:02d}".format(colnum))
    make_sure_path_exists(dirname)
    M=hierarchy_inf(raw,par,iter=750000,burn=50000,thin=1000)
    plot(M,path=dirname)
    df=pd.DataFrame()
    genes=np.sort(raw.Gene.unique())
    for gene in genes:
        df["r_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"r_"+gene).trace[:]
        df["K_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"K_"+gene).trace[:]
    df["x0_C{0:02d}".format(colnum)]=getattr(M,"x0").trace[:]
    df.to_csv(os.path.join(root,"C{0:02d}.txt".format(colnum)),sep="\t",index=False)
    frac_r=float(np.sum(df["r_{0}_C{1:02d}".format(genes[0],colnum)]>df["r_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["r_{0}_C{1:02d}".format(genes[0],colnum)])
    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of r: "+str(frac_r))
    frac_K=float(np.sum(df["K_{0}_C{1:02d}".format(genes[0],colnum)]>df["K_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["K_{0}_C{1:02d}".format(genes[0],colnum)])
    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of K: "+str(frac_K))

args.report=True

if args.report:
    pdf=PdfPages("DilutionReport.pdf")
    print("REPORTING...")
    # Find CXX.txt files...
    files=os.listdir(root)
    files=[f for f in files if ".txt" in f]
    print(files)
    reslist=[pd.read_csv(os.path.join(root,f),sep="\t") for f in files]
    res=pd.concat(reslist,axis=1,ignore_index=False)
    print(res.head())
    rcols=makeLong(res[[c for c in res.columns if "r_" in c]])
    Kcols=makeLong(res[[c for c in res.columns if "K_" in c]])
    x0cols=makeLong(res[[c for c in res.columns if "x0_" in c]])
    makeBoxplot(rcols)
    pdf.savefig()
    plt.close()
    makeBoxplot(Kcols)
    pdf.savefig()
    plt.close()
    makeBoxplot(x0cols)
    pdf.savefig()
    plt.close()
    rfrac=[np.mean(rcols.r[(rcols.column==col)&(rcols.gene=="HIS3")]>rcols.r[(rcols.column==col)&(rcols.gene=="RAD52")]) for col in rcols.column.unique()]
    Kfrac=[np.mean(Kcols.K[(Kcols.column==col)&(Kcols.gene=="HIS3")]>Kcols.K[(Kcols.column==col)&(Kcols.gene=="RAD52")]) for col in Kcols.column.unique()]
    fracs=pd.DataFrame({"K":Kfrac,"r":rfrac})
    fracs=pd.melt(fracs)
    fracs["column"]=range(1,13)+range(1,13)
    fracs.columns=["Fitness","Fraction HIS3 > RAD52","Column"]
    sns.set_context("poster",font_scale=1.5)
    ax=sns.lmplot("Column","Fraction HIS3 > RAD52",data=fracs,hue="Fitness", fit_reg=False, scatter_kws={"s": 100})
    ax.set(ylim=(0,1.05))
    ax.set(xlim=(0,13))
    pdf.savefig()
    plt.close()
    pdf.close()
    


        
    
    
    
    
    
    

