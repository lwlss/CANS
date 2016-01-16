from logistic_model import *
from pandas.tools.plotting import scatter_matrix as scatmat

# Stochastic nodes in the model (prior specifications)
class par:
    '''Prior parameters (ranges for uniform distributions)'''
    r_min,r_max=0.0,10.0
    K_min,K_max=0.0,1.0
    x0_min,x0_max=0.0,0.1
    tau_min,tau_max=0,5000

iters=250000
burnin=10000
thinning=100

# Comparing performance of ode and vectorised logistic using simulated, fairly typical data
data=sim(n_pred=50)

start=time.time()
M=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logistic)
print("Time taken for vectorised logistic model: "+sinceStart(start))

#start=time.time()
#M_ode=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logisticode)
#print("Time taken for numerical solution of competition ode: "+sinceStart(start))
#posteriorPriorPlots(M_ode,data,par,50)

# Diagnostic plots demonstrating convergance (without posterior predictive points)
diag=sim(n_pred=0)
M_diag=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logistic)

# Comparing fixed and varying inoculum density using simulated, fairly typical data
M_fix=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=True,logfun=logistic)

# Demonstrating identifiability problems for dead/missing strains
dead=sim(r=0,K=0.001,n_pred=50)
M_dead=inference(dead,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logistic)

plotCorrs(M,"Healthy strain (simulated data)")
plotCorrs(M_dead,"Dead or missing strain (simulated data)")

mc.Matplot.plot(M_diag)
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages("MCMCReport.pdf") as pdf:
    posteriorPriorPlots(M,data,par,50,show=False)
    pdf.savefig()
    plt.close()
    mc.Matplot.plot(M_diag)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_diag,data,par,50,show=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M,data,par,50,show=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_dead,dead,par,50,show=False)
    pdf.savefig()
    plt.close()
    plotCorrs(M,"Healthy strain (simulated data)",show=False)
    pdf.savefig()
    plt.close()
    plotCorrs(M_dead,"Dead or missing strain (simulated data)",show=False)
    pdf.savefig()
    plt.close()


# Read in some read Colonyzer data for inference
class realData():
    def __init__(self,fname="../../data/RawData.txt"):
        self.raw=pd.read_csv(fname,sep="\t")
