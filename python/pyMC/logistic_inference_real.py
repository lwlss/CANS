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

iters=25000
burnin=1000
thinning=10

data=realData(row=12,col=12,n_pred=50)
inocVal=0.00001

start=time.time()
M=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=False,logfun=logistic)
print("Time taken for vectorised logistic model: "+sinceStart(start))

# Comparing fixed and varying inoculum density using simulated, fairly typical data
M_fix=inference(data,par,iter=iters,burn=burnin,thin=thinning,fixInoc=True,inocVal=inocVal,logfun=logistic)

with PdfPages("MCMCReport_Real.pdf") as pdf:
    posteriorPriorPlots(M,data,par,50,show=False,main="Inferring x0, real data",simulated=False)
    pdf.savefig()
    plt.close()
    posteriorPriorPlots(M_fix,data,par,50,show=False,main="Fixing x0, real data",simulated=False)
    pdf.savefig()
    plt.close()
    plotCorrs(M,"Real data",show=False)
    pdf.savefig()
    plt.close()
    comparePosteriors(M,M_fix,data,main="Effect of fixing initial condition",lab1="IC varies",lab2="IC fixed",simulated=False)
    pdf.savefig()
    plt.close()
