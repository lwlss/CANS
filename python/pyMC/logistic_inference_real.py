from logistic_model import *
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
        
# Stochastic nodes in the model (prior specifications)
class par:
    '''Prior parameters (ranges for uniform distributions)'''
    r_min,r_max=0.0,10.0
    K_min,K_max=0.0,1.0
    x0_min,x0_max=0.0,0.1
    tau_min,tau_max=0,1500000
    v_min,v_max=0.1,10.0

iters=510000
burnin=10000
thinning=200

data=realData(row=12,col=12,n_pred=50)
inocVal=0.00001

start=time.time()
M=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logistic)
print("Time taken for vectorised logistic model: "+sinceStart(start))

# Comparing fixed and varying inoculum density using simulated, fairly typical data
M_fix=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=True,inocVal=inocVal,logfun=logistic)

M_glog=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,inocVal=inocVal,genLog=True)
M_glog_fix=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=True,inocVal=inocVal,genLog=True)

with PdfPages("MCMCReport_Real.pdf") as pdf:
    posteriorPriorPlots(M,data,par,50,show=False,main="Inferring x0, real data, logistic model",simulated=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_fix,data,par,50,show=False,main="Fixing x0, real data, logistic model",simulated=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_glog,data,par,50,show=False,main="Inferring x0, real data, gen. logistic model",simulated=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_glog_fix,data,par,50,show=False,main="Fixing x0, real data, gen. logistic model",simulated=False)
    pdf.savefig()
    plt.close()
    plotCorrs(M,"Inferring x0, real data, logistic model",show=False,maxsamp=1000)
    pdf.savefig()
    plt.close()
    plotCorrs(M_fix,"Fixing x0, real data, logistic model",show=False,maxsamp=1000)
    pdf.savefig()
    plt.close()
    plotCorrs(M_glog,"Inferring x0, real data, gen. logistic model",show=False,maxsamp=1000)
    pdf.savefig()
    plt.close()
    plotCorrs(M_glog_fix,"Fixing x0, real data, gen. logistic model",show=False,maxsamp=1000)
    pdf.savefig()
    plt.close()
    comparePosteriors2([M,M_fix,M_glog,M_glog_fix],["Log., x0 varies","Log., fixed x0","GLog., x0 varies", "GLog, fixed x0"],["red","blue","green","orange"],main="Comparing fitness estimates")
    pdf.savefig()
    plt.close()
