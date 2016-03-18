from logistic_model import *
import seaborn as sns
import argparse
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.cm as cm
import matplotlib.patches as mpatches

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
        if "K" in var:
            ax.set_ylim(0,0.2)
        if "r" in var:
            ax.set_ylim(0,6.5)
        if "x0" in var:
            ax.set_ylim(0,0.006)
        if "mdrmdp" in var:
            ax.set_ylim(0,70)
    else:
        ax = sns.boxplot(x="column",y=var,data=longdf)
        ax.set(yscale="log")
        ax.set_ylim(1e-4,)
        
    #plt.xticks(rotation=90)
    #plt.show()    

parser = argparse.ArgumentParser(description='Dilution Experiment')
parser.add_argument("-c","--column", type=int ,help='Plate column number')
parser.add_argument("-r","--report", help="Summarise completed inference",action="store_true")
parser.add_argument("-f","--fixed", help="Fix inoculum density estimate for all spots in a column",action="store_true")
args = parser.parse_args()

#args.column=1
#args.fixed=True
#args.report=True

if args.fixed:
    root="DilutionsFixed"
else:
    root="Dilutions"
    
fname="../../data/dilution/RawData.txt"
maxc=8 # Highest column number to consider in report

if args.column:
    colnum=int(args.column)
    print("Column {}".format(colnum))
    raw=pd.read_csv(fname,sep="\t")
    raw=raw[raw.Column==colnum]
    make_sure_path_exists(root)
    dirname=os.path.join(root,"C{0:02d}".format(colnum))
    make_sure_path_exists(dirname)
    if args.fixed:
        M=hierarchy_inf(raw,par,iter=500000,burn=10000,thin=500)
    else:
        M=hierarchy_inf_x0(raw,par,iter=500000,burn=10000,thin=500)

    print("Diagnostic plots")
    plot(M,path=dirname)
    df=pd.DataFrame()
    genes=np.sort(raw.Gene.unique())
    for gene in genes:
        if args.fixed:
            df["x0_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"x0").trace[:]
        else:
            df["x0_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"x0_"+gene).trace[:]
        df["r_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"r_"+gene).trace[:]
        df["K_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"K_"+gene).trace[:]
    df["x0_C{0:02d}".format(colnum)]=getattr(M,"x0").trace[:]
    df.to_csv(os.path.join(root,"C{0:02d}.txt".format(colnum)),sep="\t",index=False)
    frac_r=float(np.sum(df["r_{0}_C{1:02d}".format(genes[0],colnum)]>df["r_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["r_{0}_C{1:02d}".format(genes[0],colnum)])
    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of r: "+str(frac_r))
    frac_K=float(np.sum(df["K_{0}_C{1:02d}".format(genes[0],colnum)]>df["K_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["K_{0}_C{1:02d}".format(genes[0],colnum)])
    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of K: "+str(frac_K)) 

if args.report:
    pdf=PdfPages(root+".pdf")
    print("REPORTING...")
    # Find CXX.txt files...
    files=os.listdir(root)
    files=[f for f in files if ".txt" in f]
    print(files)
    reslist=[pd.read_csv(os.path.join(root,f),sep="\t") for f in files]
    res=pd.concat(reslist,axis=1,ignore_index=False)
    # Discard high dilutions
    
    res=res[[c for c in res.columns if int(c[-2:])<=maxc]]
    print(res.head())
    rcols=makeLong(res[[c for c in res.columns if "r_" in c]])
    Kcols=makeLong(res[[c for c in res.columns if "K_" in c]])
    x0cols=makeLong(res[[c for c in res.columns if "x0_" in c and c.count("_")==1]])
    if not args.fixed:
        x0genes=makeLong(res[[c for c in res.columns if "x0_" in c and c.count("_")==2]])
    if args.fixed:
        x0his3=x0cols.copy()
        x0his3["gene"]="HIS3"
        x0rad52=x0cols.copy()
        x0rad52["gene"]="RAD52"
        x0genes=pd.concat([x0his3,x0rad52])
        x0genes=x0genes.reset_index(drop=True)
    print(len(x0genes.x0))
    print(len(rcols.r))
    print(len(Kcols.K))
    mdrvec=mdr(x0genes.x0,rcols.r,Kcols.K,1.0)
    mdpvec=mdp(x0genes.x0,Kcols.K)
    mdrmdpvec=mdrvec*mdpvec
    mdrcols=pd.DataFrame({"fname":rcols.fname,"mdr":mdrvec,"var":"mdr","gene":rcols.gene,"column":rcols.column})
    mdpcols=pd.DataFrame({"fname":rcols.fname,"mdp":mdpvec,"var":"mdp","gene":rcols.gene,"column":rcols.column})
    mdrmdpcols=pd.DataFrame({"fname":rcols.fname,"mdrmdp":mdrmdpvec,"var":"mdrmdp","gene":rcols.gene,"column":rcols.column})
    makeBoxplot(rcols)
    pdf.savefig()
    plt.close()
    makeBoxplot(Kcols)
    pdf.savefig()
    plt.close()
    makeBoxplot(mdrmdpcols)
    pdf.savefig()
    plt.close()
    makeBoxplot(x0cols)
    pdf.savefig()
    plt.close()
    makeBoxplot(x0genes)
    pdf.savefig()
    plt.close()
    rfrac=[np.mean(rcols.r[(rcols.column==col)&(rcols.gene=="HIS3")]>rcols.r[(rcols.column==col)&(rcols.gene=="RAD52")]) for col in rcols.column.unique()]
    Kfrac=[np.mean(Kcols.K[(Kcols.column==col)&(Kcols.gene=="HIS3")]>Kcols.K[(Kcols.column==col)&(Kcols.gene=="RAD52")]) for col in Kcols.column.unique()]
    x0frac=[np.mean(x0genes.x0[(x0genes.column==col)&(x0genes.gene=="HIS3")]>x0genes.x0[(x0genes.column==col)&(x0genes.gene=="RAD52")]) for col in x0genes.column.unique()]
    mdrfrac=[np.mean(mdrcols.mdr[(mdrcols.column==col)&(mdrcols.gene=="HIS3")]>mdrcols.mdr[(mdrcols.column==col)&(mdrcols.gene=="RAD52")]) for col in mdrcols.column.unique()]
    mdpfrac=[np.mean(mdpcols.mdp[(mdpcols.column==col)&(mdpcols.gene=="HIS3")]>mdpcols.mdp[(mdpcols.column==col)&(mdpcols.gene=="RAD52")]) for col in mdpcols.column.unique()]
    mdrmdpfrac=[np.mean(mdrmdpcols.mdrmdp[(mdrmdpcols.column==col)&(mdrmdpcols.gene=="HIS3")]>mdrmdpcols.mdrmdp[(mdrmdpcols.column==col)&(mdrmdpcols.gene=="RAD52")]) for col in mdrmdpcols.column.unique()]
    fracs=pd.DataFrame({"K":Kfrac,"r":rfrac,"mdr":mdrfrac,"mdp":mdpfrac,"mdrmdp":mdrmdpfrac,"x0":x0frac})
    fracs=pd.melt(fracs)
    fracs["column"]=list(range(1,maxc+1))+list(range(1,maxc+1))+list(range(1,maxc+1))+list(range(1,maxc+1))+list(range(1,maxc+1))+list(range(1,maxc+1))
    fracs.columns=["Fitness","Fraction HIS3 > RAD52","Column"]

    sns.set_context("poster",font_scale=1.0)
    fdefs=fracs.Fitness.unique()
    colors = cm.rainbow(np.linspace(0, 1, len(fdefs)))
    patches=[mpatches.Patch(color=c,label=l) for c,l in zip(colors,fdefs)]
    for f,col in zip(fdefs,colors):
        frac=fracs[fracs.Fitness==f]
        plt.scatter(frac.Column,frac['Fraction HIS3 > RAD52'],c=col,s=125,linewidth=0)
        plt.plot(frac.Column,frac['Fraction HIS3 > RAD52'],c=col,lw=3)
    plt.legend(handles=patches)
    plt.xlabel("Column number (dilution)")
    plt.ylabel("Proportion HIS3 > RAD52")
    plt.ylim(0.0,1.0)
    if args.fixed:
        plt.suptitle("Learning about x0 for each column only",fontsize=20)
    else:
        plt.suptitle("Learning about x0 for each column and each spot",fontsize=20)
    
    pdf.savefig()
    plt.close()
    # Correlation plots for each column
    sns.set_context("paper",font_scale=0.5)
    plt.rcParams.update({'font.size': 5})
    for res,fname in zip(reslist,files):
        res.columns=[r[0:-4] for r in res.columns]
        scat=scatmat(res.head(100),diagonal="kde",s=5)
        fntsize=4
        [plt.setp(item.xaxis.get_majorticklabels(), 'size', fntsize) for item in scat.ravel()]
        [plt.setp(item.yaxis.get_majorticklabels(), 'size', fntsize) for item in scat.ravel()]
        plt.suptitle(fname)
        pdf.savefig()
        plt.close()
        
    pdf.close()
    


        
    
    
    
    
    
    

