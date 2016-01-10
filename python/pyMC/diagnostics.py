import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import pymc as mc

def summarisePred(p,conf=0.95):
    lowerperc=100.0*(1.0-conf)/2.0
    upperperc=100.0-lowerperc
    res={}
    res['low']=[np.percentile(p.trace[:,i],lowerperc) for i in range(p.shape[0])]
    res['med']=[np.percentile(p.trace[:,i],50.0) for i in range(p.shape[0])]
    res['up']=[np.percentile(p.trace[:,i],upperperc) for i in range(p.shape[0])]
    return(res)

def predictPlots(M,splitPlots=False):
    mc.Matplot.plot(M.pred)
    if splitPlots:
        for i in range(0,M.pred.shape[0]):
            Matplot.plot(M.pred.trace[:,i],"pred_%01d"%i)
    
def posteriorPriorPlots(M,sim,par,bnum=50):
    nodenames=[x.__name__ for x in M._variables_to_tally]
    pred=summarisePred(M.pred)
    fig,ax=plt.subplots(2,3,figsize=(21,14))
    
    ax[0,0].scatter(sim.t_exp,sim.x_exp)
    ax[0,0].set_xlabel('Time since inoculation (d)')
    ax[0,0].set_ylabel('Population size (AU)')
    ax[0,0].set_ylim([min(pred["low"]),max(pred["up"])])

    ax[0,1].scatter(sim.t_exp,sim.x_obs)
    ax[0,1].plot(sim.t_pred,pred["med"],color="blue")
    ax[0,1].plot(sim.t_pred,pred["low"],color="blue",linestyle="dashed")
    ax[0,1].plot(sim.t_pred,pred["up"],color="blue",linestyle="dashed")
    ax[0,1].set_xlabel('Time since inoculation (d)')
    ax[0,1].set_ylabel('Population size (AU)')
    ax[0,1].set_ylim([min(pred["low"]),max(pred["up"])])

    if 'x0' in nodenames: 
        x0_pdf=gaussian_kde(M.trace('x0')[:])
        x0_min,x0_max=np.percentile(M.trace('x0')[:],[0,100])
        x0_range=np.linspace(par.x0_min,par.x0_max,500)
        x0_dens=x0_pdf(x0_range)
        ax[0,2].hist(M.trace('x0')[:],bins=np.linspace(par.x0_min,par.x0_max,bnum),normed=True,color="skyblue")
        ax[0,2].plot(x0_range,x0_dens,'r',color="blue")
        ax[0,2].vlines(sim.x0_true,0,max(x0_dens),linestyles='dashed')
        ax[0,2].set_xlabel('x0 (AU)')
        ax[0,2].set_ylabel('Density')
        yval=1.0/(par.x0_max-par.x0_min)
        ax[0,2].vlines([par.x0_min,par.x0_max],0,yval,color="red")
        ax[0,2].hlines(yval,par.x0_min,par.x0_max,color="red")

    r_pdf=gaussian_kde(M.trace('r')[:])
    r_min,r_max=np.percentile(M.trace('r')[:],[0,100])
    r_range=np.linspace(par.r_min,par.r_max,500)
    r_dens=r_pdf(r_range)    
    ax[1,0].hist(M.trace('r')[:],bins=np.linspace(par.r_min,par.r_max,bnum),normed=True,color="skyblue")
    ax[1,0].plot(r_range,r_dens,'r',color="blue")
    ax[1,0].vlines(sim.r_true,0,max(r_dens),linestyles='dashed')
    ax[1,0].set_xlabel('r (1/d)')
    ax[1,0].set_ylabel('Density')
    yval=1.0/(par.r_max-par.r_min)
    ax[1,0].vlines([par.r_min,par.r_max],0,yval,color="red")
    ax[1,0].hlines(yval,par.r_min,par.r_max,color="red")

    K_pdf=gaussian_kde(M.trace('K')[:])
    K_min,K_max=np.percentile(M.trace('K')[:],[0,100])
    K_range=np.linspace(par.K_min,par.K_max,500)
    K_dens=K_pdf(K_range)    
    ax[1,1].hist(M.trace('K')[:],bins=np.linspace(par.K_min,par.K_max,bnum),normed=True,color="skyblue")
    ax[1,1].plot(K_range,K_dens,'r',color="blue")
    ax[1,1].vlines(sim.K_true,0,max(K_dens),linestyles='dashed')
    ax[1,1].set_xlabel('K (AU)')
    ax[1,1].set_ylabel('Density')
    yval=1.0/(par.K_max-par.K_min)
    ax[1,1].vlines([par.K_min,par.K_max],0,yval,color="red")
    ax[1,1].hlines(yval,par.K_min,par.K_max,color="red")
    
    tau_pdf=gaussian_kde(M.trace('tau')[:])
    tau_min,tau_max=np.percentile(M.trace('tau')[:],[0,100])
    tau_range=np.linspace(par.tau_min,par.tau_max,500)
    tau_dens=tau_pdf(tau_range)
    ax[1,2].hist(M.trace('tau')[:],bins=np.linspace(par.tau_min,par.tau_max,bnum),normed=True,color="skyblue")
    ax[1,2].plot(tau_range,tau_dens,'r',color="blue")
    ax[1,2].vlines(sim.tau_true,0,max(tau_dens),linestyles='dashed')
    ax[1,2].set_xlabel('tau')
    ax[1,2].set_ylabel('Density')
    yval=1.0/(par.tau_max-par.tau_min)
    ax[1,2].vlines([par.tau_min,par.tau_max],0,yval,color="red")
    ax[1,2].hlines(yval,par.tau_min,par.tau_max,color="red")
    
    plt.show()
